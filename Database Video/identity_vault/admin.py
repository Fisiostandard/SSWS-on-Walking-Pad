from django.contrib import admin
from .models import PatientIdentity


@admin.register(PatientIdentity)
class PatientIdentityAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'pseudo_id', 'date_of_birth', 'phone', 'referring_doctor']
    search_fields = ['last_name', 'first_name', 'pseudo_id', 'fiscal_code', 'phone']
    list_filter = ['referring_doctor']
    readonly_fields = ['created_at', 'updated_at']

    # Forza l'uso del database identity_db
    using = 'identity_db'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
