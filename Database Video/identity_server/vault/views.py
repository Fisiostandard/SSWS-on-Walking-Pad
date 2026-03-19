import json
import os
from functools import wraps

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import PatientIdentity

API_TOKEN = os.environ.get('API_TOKEN', '')


def require_token(view_func):
    """Verifica che la richiesta contenga il token API corretto."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token or token != API_TOKEN:
            return JsonResponse({'error': 'Non autorizzato'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@require_token
@require_http_methods(["POST"])
def register(request):
    """
    Registra un nuovo paziente nella tabella di raccordo.
    Input JSON: {"pseudo_id": "PAZ-...", "fiscal_code": "RSSMRA58...", "last_name": "Rossi", "first_name": "Mario"}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    required = ['pseudo_id', 'fiscal_code', 'last_name', 'first_name']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'error': f'Campi mancanti: {", ".join(missing)}'}, status=400)

    # Controlla se il CF esiste già
    existing = PatientIdentity.objects.filter(fiscal_code=data['fiscal_code'].upper()).first()
    if existing:
        return JsonResponse({
            'status': 'exists',
            'pseudo_id': existing.pseudo_id,
            'message': 'Paziente già registrato'
        })

    patient = PatientIdentity.objects.create(
        pseudo_id=data['pseudo_id'],
        fiscal_code=data['fiscal_code'].upper().strip(),
        last_name=data['last_name'].strip(),
        first_name=data['first_name'].strip(),
    )

    return JsonResponse({
        'status': 'created',
        'pseudo_id': patient.pseudo_id,
    }, status=201)


@csrf_exempt
@require_token
@require_http_methods(["POST"])
def lookup(request):
    """
    Cerca un paziente per codice fiscale e restituisce il pseudo_id.
    Input JSON: {"fiscal_code": "RSSMRA58..."}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    fiscal_code = data.get('fiscal_code', '').upper().strip()
    if not fiscal_code:
        return JsonResponse({'error': 'fiscal_code richiesto'}, status=400)

    patient = PatientIdentity.objects.filter(fiscal_code=fiscal_code).first()
    if not patient:
        return JsonResponse({'error': 'Paziente non trovato'}, status=404)

    return JsonResponse({
        'pseudo_id': patient.pseudo_id,
        'last_name': patient.last_name,
        'first_name': patient.first_name,
    })


@csrf_exempt
@require_token
@require_http_methods(["POST"])
def lookup_or_create(request):
    """
    Cerca un paziente per codice fiscale. Se non esiste, lo crea.
    Restituisce sempre un pseudo_id.
    Input JSON: {"fiscal_code": "RSSMRA58...", "last_name": "Rossi", "first_name": "Mario"}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    fiscal_code = data.get('fiscal_code', '').upper().strip()
    last_name = data.get('last_name', '').strip()
    first_name = data.get('first_name', '').strip()

    if not fiscal_code:
        return JsonResponse({'error': 'fiscal_code obbligatorio'}, status=400)
    if not last_name or not first_name:
        return JsonResponse({'error': 'last_name e first_name obbligatori'}, status=400)

    # Cerca per CF
    existing = PatientIdentity.objects.filter(fiscal_code=fiscal_code).first()
    if existing:
        return JsonResponse({
            'status': 'found',
            'pseudo_id': existing.pseudo_id,
            'created': False,
        })

    # Crea nuovo: genera pseudo_id
    import uuid
    from django.utils import timezone as tz
    date_str = tz.now().strftime('%Y%m%d')
    random_hex = uuid.uuid4().hex[:4].upper()
    pseudo_id = f"PAZ-{date_str}-{random_hex}"

    patient = PatientIdentity.objects.create(
        pseudo_id=pseudo_id,
        fiscal_code=fiscal_code,
        last_name=last_name,
        first_name=first_name,
    )

    return JsonResponse({
        'status': 'created',
        'pseudo_id': patient.pseudo_id,
        'created': True,
    }, status=201)


@csrf_exempt
@require_token
@require_http_methods(["POST"])
def search(request):
    """
    Cerca pazienti per cognome (parziale).
    Input JSON: {"query": "Ross"}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON non valido'}, status=400)

    query = data.get('query', '').strip()
    if len(query) < 2:
        return JsonResponse({'error': 'Inserire almeno 2 caratteri'}, status=400)

    patients = PatientIdentity.objects.filter(
        last_name__icontains=query
    )[:20]

    results = [{
        'pseudo_id': p.pseudo_id,
        'last_name': p.last_name,
        'first_name': p.first_name,
        'fiscal_code': p.fiscal_code,
    } for p in patients]

    return JsonResponse({'results': results})
