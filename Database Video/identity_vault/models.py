from django.db import models


class PatientIdentity(models.Model):
    """
    Tabella di raccordo: collega l'ID pseudonimizzato all'identità reale.
    Vive in un DATABASE SEPARATO (identity_db) rispetto ai dati clinici.
    """
    pseudo_id = models.CharField(
        max_length=20, unique=True, db_index=True,
        help_text="ID pseudonimizzato (deve corrispondere a Patient.pseudo_id)"
    )
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Cognome")
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Data di nascita"
    )
    phone = models.CharField(
        max_length=30, blank=True, verbose_name="Telefono"
    )
    email = models.EmailField(blank=True, verbose_name="Email")
    fiscal_code = models.CharField(
        max_length=16, blank=True, verbose_name="Codice Fiscale"
    )
    referring_doctor = models.CharField(
        max_length=200, blank=True, verbose_name="Medico prescrittore"
    )
    notes = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_identity'
        verbose_name = 'Identità Paziente'
        verbose_name_plural = 'Identità Pazienti'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.pseudo_id})"
