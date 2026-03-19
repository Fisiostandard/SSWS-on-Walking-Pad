from django.contrib import admin
from .models import Patient, Session, ClinicalTest, Video, ShareLink, AccessLog
from .api_auth import APIToken


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0
    show_change_link = True


class ClinicalTestInline(admin.TabularInline):
    model = ClinicalTest
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pseudo_id', 'created_at', 'created_by']
    search_fields = ['pseudo_id', 'notes']
    readonly_fields = ['pseudo_id', 'created_at']
    inlines = [SessionInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'operator', 'pain_level', 'assistive_device']
    list_filter = ['date', 'operator']
    search_fields = ['patient__pseudo_id', 'notes']
    inlines = [ClinicalTestInline, VideoInline]

    def save_model(self, request, obj, form, change):
        if not change and not obj.operator:
            obj.operator = request.user
        super().save_model(request, obj, form, change)


@admin.register(ClinicalTest)
class ClinicalTestAdmin(admin.ModelAdmin):
    list_display = ['session', 'test_type', 'trial_number', 'value', 'unit']
    list_filter = ['test_type']
    search_fields = ['session__patient__pseudo_id']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['session', 'title', 'face_blurred', 'duration_seconds', 'uploaded_at']
    list_filter = ['face_blurred']
    search_fields = ['session__patient__pseudo_id', 'title']


@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ['patient', 'recipient_type', 'recipient_name', 'is_valid', 'access_count', 'expires_at', 'is_revoked']
    list_filter = ['recipient_type', 'is_revoked']
    search_fields = ['patient__pseudo_id', 'recipient_name']
    readonly_fields = ['token', 'access_count', 'created_at']
    actions = ['revoke_links']

    @admin.action(description="Revoca i link selezionati")
    def revoke_links(self, request, queryset):
        queryset.update(is_revoked=True)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['share_link', 'accessed_at', 'ip_address', 'success']
    list_filter = ['success']
    readonly_fields = ['share_link', 'accessed_at', 'ip_address', 'user_agent', 'success']


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'created_at', 'last_used_at']
    list_filter = ['is_active']
    readonly_fields = ['token', 'created_at', 'last_used_at']
    actions = ['deactivate_tokens']

    @admin.action(description="Disattiva i token selezionati")
    def deactivate_tokens(self, request, queryset):
        queryset.update(is_active=False)
