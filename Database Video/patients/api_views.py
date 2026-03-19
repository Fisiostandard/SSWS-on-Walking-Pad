"""
API REST per ricezione dati dal WalkingPad treadmill.
Endpoint protetto con Bearer token (vedi api_auth.py).
"""
import json
import hashlib
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Patient, Session, ClinicalTest
from .api_auth import require_api_token

logger = logging.getLogger('patients.api')


@csrf_exempt
@require_api_token
@require_http_methods(["POST"])
def receive_treadmill_session(request):
    """
    Riceve i dati di una sessione treadmill dal WalkingPad server.

    Il Flask server invia solo il pseudo_id (mai nomi reali).
    La risoluzione nome → pseudo_id avviene lato Flask via identity vault.

    Payload JSON:
    {
        "pseudo_id": "PAZ-20260319-A7F2",     # obbligatorio (ottenuto dal vault)
        "session_date": "2026-03-19",           # opzionale, default=oggi
        "trial_number": 1,                      # opzionale, default=auto-increment
        "ssws_kmh": 4.23,                       # velocità SSWS in km/h
        "ssws_ms": 1.175,                       # velocità SSWS in m/s (valore primario)
        "ssws_method": "manual",                # "manual" | "auto"
        "duration_s": 125.3,
        "distance_m": 487.0,
        "steps": 312,
        "max_speed_kmh": 5.1,
        "max_speed_setting_kmh": 6.0,
        "sensitivity": 1,
        "tamper_detected": false,
        "session_uuid": "uuid-v4",              # idempotency key
        "log": [...],                           # full speed log
        "ssws_markers": [...],
        "notes": ""
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    # ── Validazione campi obbligatori ──
    pseudo_id = data.get('pseudo_id', '').strip()
    if not pseudo_id:
        return JsonResponse({'error': 'pseudo_id obbligatorio'}, status=400)

    ssws_kmh = data.get('ssws_kmh')
    ssws_ms = data.get('ssws_ms')
    ssws_markers = data.get('ssws_markers', [])

    if not ssws_kmh and not ssws_markers:
        return JsonResponse(
            {'error': 'Almeno ssws_kmh o ssws_markers deve essere presente'},
            status=400
        )

    # Calcola ssws_ms se non fornito
    if ssws_kmh and not ssws_ms:
        ssws_ms = round(ssws_kmh / 3.6, 3)

    # ── Idempotency check ──
    session_uuid = data.get('session_uuid', '')
    if session_uuid:
        existing = ClinicalTest.objects.filter(
            test_type='TREADMILL_SSWS',
            extra_data__session_uuid=session_uuid,
        ).first()
        if existing:
            return JsonResponse({
                'status': 'already_exists',
                'pseudo_id': pseudo_id,
                'test_id': existing.id,
                'message': 'Sessione già registrata (idempotency key)',
            })

    # ── Trova o crea paziente ──
    try:
        patient = Patient.objects.get(pseudo_id=pseudo_id)
    except Patient.DoesNotExist:
        # Paziente nuovo: crea con il pseudo_id fornito dal vault
        patient = Patient(pseudo_id=pseudo_id, created_by=request.api_user)
        patient.save()
        logger.info("Nuovo paziente creato: %s", pseudo_id)

    # ── Trova o crea sessione ──
    session_date_str = data.get('session_date', '')
    if session_date_str:
        try:
            from datetime import date as date_type
            parts = session_date_str.split('-')
            session_date = date_type(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, IndexError):
            return JsonResponse({'error': 'Formato session_date non valido (YYYY-MM-DD)'}, status=400)
    else:
        session_date = timezone.now().date()

    session, _ = Session.objects.get_or_create(
        patient=patient,
        date=session_date,
        defaults={'operator': request.api_user},
    )

    # ── Trial number auto-increment ──
    trial_number = data.get('trial_number')
    if not trial_number:
        last_trial = ClinicalTest.objects.filter(
            session=session, test_type='TREADMILL_SSWS'
        ).order_by('-trial_number').first()
        trial_number = (last_trial.trial_number + 1) if last_trial else 1

    # ── Componi extra_data ──
    log_data = data.get('log', [])
    log_hash = ''
    if log_data:
        log_json = json.dumps(log_data, sort_keys=True)
        log_hash = hashlib.sha256(log_json.encode()).hexdigest()

    extra_data = {
        'source': 'walkingpad_treadmill',
        'device': 'Kingsmith WalkingPad',
        'session_uuid': session_uuid,
        'ssws_kmh': ssws_kmh,
        'ssws_method': data.get('ssws_method', 'unknown'),
        'max_speed_setting_kmh': data.get('max_speed_setting_kmh'),
        'sensitivity': data.get('sensitivity'),
        'duration_s': data.get('duration_s'),
        'distance_m': data.get('distance_m'),
        'steps': data.get('steps'),
        'max_speed_reached_kmh': data.get('max_speed_kmh'),
        'tamper_detected': data.get('tamper_detected', False),
        'ssws_markers': ssws_markers,
        'log_hash_sha256': log_hash,
        'log_points': len(log_data),
        'full_log': log_data,
    }

    # ── Crea ClinicalTest ──
    test = ClinicalTest.objects.create(
        session=session,
        test_type='TREADMILL_SSWS',
        trial_number=trial_number,
        value=ssws_ms,
        unit='m/s',
        extra_data=extra_data,
        notes=data.get('notes', ''),
    )

    logger.info(
        "Treadmill SSWS salvata: %s, trial #%d, %.3f m/s (%.2f km/h)",
        pseudo_id, trial_number, ssws_ms, ssws_kmh or 0
    )

    return JsonResponse({
        'status': 'created',
        'pseudo_id': pseudo_id,
        'session_id': session.id,
        'session_date': str(session_date),
        'test_id': test.id,
        'trial_number': trial_number,
        'ssws_ms': ssws_ms,
    }, status=201)
