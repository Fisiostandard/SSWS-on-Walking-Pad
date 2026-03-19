"""
Autenticazione API tramite Bearer token.
I token vengono creati e gestiti dall'admin Django.
"""
import secrets
from functools import wraps

from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone


class APIToken(models.Model):
    """Token API per autenticazione machine-to-machine."""
    token = models.CharField(
        max_length=64, unique=True, editable=False, db_index=True,
        help_text="Generato automaticamente"
    )
    name = models.CharField(
        max_length=100,
        help_text="Etichetta descrittiva (es. 'WalkingPad Clinica Firenze')"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='api_tokens',
        help_text="Operatore associato a questo token"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    def __str__(self):
        status = "attivo" if self.is_active else "disattivato"
        return f"{self.name} ({status})"


def require_api_token(view_func):
    """Decoratore: verifica Bearer token e attacca request.api_user."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization header mancante'}, status=401)

        token_value = auth_header[7:]  # Strip "Bearer "
        try:
            api_token = APIToken.objects.select_related('user').get(
                token=token_value, is_active=True
            )
        except APIToken.DoesNotExist:
            return JsonResponse({'error': 'Token non valido o disattivato'}, status=401)

        # Aggiorna ultimo utilizzo
        api_token.last_used_at = timezone.now()
        api_token.save(update_fields=['last_used_at'])

        request.api_user = api_token.user
        request.api_token = api_token
        return view_func(request, *args, **kwargs)
    return wrapper
