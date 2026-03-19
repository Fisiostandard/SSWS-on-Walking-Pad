from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from .models import ShareLink, AccessLog, Video


def share_access(request, token):
    """Pagina di accesso al link condiviso — richiede password."""
    link = get_object_or_404(ShareLink, token=token)

    # Controlla validità
    if not link.is_valid:
        return render(request, 'patients/share_expired.html', {
            'reason': 'revocato' if link.is_revoked else
                      'limite accessi raggiunto' if link.access_count >= link.max_access_count else
                      'scaduto'
        })

    error = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        ip = _get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if check_password(password, link.password_hash):
            # Password corretta — registra accesso e mostra contenuto
            link.access_count += 1
            link.save(update_fields=['access_count'])
            AccessLog.objects.create(
                share_link=link,
                ip_address=ip,
                user_agent=user_agent,
                success=True,
            )
            # Salva in sessione per non richiedere password ad ogni refresh
            request.session[f'share_{token}'] = True
            return _render_shared_content(request, link)
        else:
            AccessLog.objects.create(
                share_link=link,
                ip_address=ip,
                user_agent=user_agent,
                success=False,
            )
            error = "Password errata."

    # Se già autenticato in sessione
    if request.session.get(f'share_{token}'):
        return _render_shared_content(request, link)

    return render(request, 'patients/share_login.html', {
        'token': token,
        'recipient_type': link.get_recipient_type_display(),
        'error': error,
    })


def share_video_stream(request, token, video_id):
    """Streaming del video — solo se autenticato via sessione."""
    link = get_object_or_404(ShareLink, token=token)

    if not link.is_valid:
        raise Http404

    if not request.session.get(f'share_{token}'):
        raise Http404

    video = get_object_or_404(Video, id=video_id, session__patient=link.patient)

    if not video.file:
        raise Http404

    response = FileResponse(video.file.open('rb'), content_type='video/mp4')
    response['Content-Disposition'] = f'inline; filename="{video.title or "video"}.mp4"'
    # Impedisci download diretto
    response['X-Content-Type-Options'] = 'nosniff'
    return response


def _render_shared_content(request, link):
    """Mostra i video e i test della sessione condivisa."""
    if link.session:
        sessions = [link.session]
    else:
        sessions = link.patient.sessions.all()

    session_data = []
    for session in sessions:
        session_data.append({
            'session': session,
            'tests': session.tests.all(),
            'videos': session.videos.filter(face_blurred=True),
        })

    return render(request, 'patients/share_content.html', {
        'link': link,
        'patient_id': link.patient.pseudo_id,
        'session_data': session_data,
        'token': link.token,
    })


def _get_client_ip(request):
    """Estrai l'IP del client (gestisce proxy/load balancer)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')
