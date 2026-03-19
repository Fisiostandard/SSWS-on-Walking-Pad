from django.db import models


class PatientIdentity(models.Model):
    """Tabella di raccordo: pseudo_id <-> identità reale del paziente."""
    pseudo_id = models.CharField(max_length=20, unique=True, db_index=True)
    fiscal_code = models.CharField(max_length=16, unique=True, db_index=True, verbose_name="Codice Fiscale")
    last_name = models.CharField(max_length=100, verbose_name="Cognome")
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_identity'
        verbose_name = 'Identità Paziente'
        verbose_name_plural = 'Identità Pazienti'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.pseudo_id})"
