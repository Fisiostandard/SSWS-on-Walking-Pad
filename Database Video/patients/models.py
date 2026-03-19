import uuid
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Patient(models.Model):
    """Paziente pseudonimizzato. Nessun dato identificativo diretto."""
    pseudo_id = models.CharField(
        max_length=20, unique=True, editable=False,
        help_text="ID pseudonimizzato (es. PAZ-20260319-A7F2)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Note cliniche generali (NO nome/cognome/CF)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='patients_created'
    )

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pseudo_id:
            date_str = timezone.now().strftime('%Y%m%d')
            random_hex = uuid.uuid4().hex[:4].upper()
            self.pseudo_id = f"PAZ-{date_str}-{random_hex}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pseudo_id


class Session(models.Model):
    """Una sessione di valutazione per un paziente."""
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='sessions'
    )
    date = models.DateField(help_text="Data della sessione")
    operator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sessions_operated'
    )
    # Condizioni del paziente
    pain_level = models.IntegerField(
        null=True, blank=True,
        help_text="Livello dolore VAS 0-10"
    )
    medications = models.TextField(
        blank=True, help_text="Farmaci assunti"
    )
    footwear = models.CharField(
        max_length=100, blank=True,
        help_text="Tipo di calzatura"
    )
    assistive_device = models.CharField(
        max_length=100, blank=True,
        help_text="Ausilio deambulazione (nessuno, stampella, deambulatore...)"
    )
    notes = models.TextField(blank=True, help_text="Note sulla sessione")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.pseudo_id} — {self.date}"


class ClinicalTest(models.Model):
    """Risultato di un test clinico (SSWS, TUG, Romberg, ecc.)."""
    TEST_TYPES = [
        ('10MWT', '10-Meter Walk Test'),
        ('TREADMILL_SSWS', 'Treadmill SSWS'),
        ('TUG', 'Timed Up and Go'),
        ('ROMBERG', 'Test di Romberg'),
        ('6MWT', '6-Minute Walk Test'),
        ('BBS', 'Berg Balance Scale'),
        ('OTHER', 'Altro'),
    ]

    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='tests'
    )
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    trial_number = models.IntegerField(
        default=1, help_text="Numero del trial (1, 2, 3...)"
    )
    value = models.FloatField(
        null=True, blank=True,
        help_text="Valore numerico principale (es. velocità m/s, tempo s)"
    )
    unit = models.CharField(
        max_length=20, default='m/s',
        help_text="Unità di misura"
    )
    extra_data = models.JSONField(
        null=True, blank=True,
        help_text="Dati aggiuntivi in formato JSON"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['test_type', 'trial_number']

    def __str__(self):
        return f"{self.session} — {self.get_test_type_display()} #{self.trial_number}: {self.value} {self.unit}"


class Video(models.Model):
    """Video del paziente con volto blurrato."""
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='videos'
    )
    title = models.CharField(
        max_length=200, blank=True,
        help_text="Descrizione breve (es. 'Treadmill trial 1')"
    )
    file = models.FileField(upload_to='videos/%Y/%m/')
    duration_seconds = models.FloatField(
        null=True, blank=True,
        help_text="Durata in secondi"
    )
    face_blurred = models.BooleanField(
        default=False,
        help_text="Il volto è stato blurrato?"
    )
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.session} — {self.title or 'Video'}"


class ShareLink(models.Model):
    """Link protetto per condividere video/dati con paziente o medico."""
    RECIPIENT_TYPES = [
        ('PATIENT', 'Paziente'),
        ('DOCTOR', 'Medico prescrittore'),
    ]

    token = models.CharField(
        max_length=64, unique=True, editable=False, db_index=True
    )
    password_hash = models.CharField(max_length=128)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='share_links'
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True,
        help_text="Se vuoto, condivide tutte le sessioni del paziente"
    )
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPES)
    recipient_name = models.CharField(
        max_length=200, blank=True,
        help_text="Nome del destinatario (es. 'Dr. Rossi')"
    )
    # Sicurezza
    expires_at = models.DateTimeField(
        help_text="Data/ora di scadenza del link"
    )
    max_access_count = models.IntegerField(
        default=50,
        help_text="Numero massimo di accessi consentiti"
    )
    access_count = models.IntegerField(default=0)
    is_revoked = models.BooleanField(default=False)
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        if self.is_revoked:
            return False
        if self.access_count >= self.max_access_count:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True

    def __str__(self):
        status = "attivo" if self.is_valid else "scaduto/revocato"
        return f"Link {self.recipient_type} per {self.patient.pseudo_id} ({status})"


class AccessLog(models.Model):
    """Log di ogni accesso a un link condiviso."""
    share_link = models.ForeignKey(
        ShareLink, on_delete=models.CASCADE, related_name='access_logs'
    )
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(
        default=True,
        help_text="False se password errata o link scaduto"
    )

    class Meta:
        ordering = ['-accessed_at']

    def __str__(self):
        return f"{self.share_link.patient.pseudo_id} — {self.accessed_at} — {self.ip_address}"


# Importa APIToken qui per renderlo visibile a Django migrations
from .api_auth import APIToken  # noqa: E402, F401
