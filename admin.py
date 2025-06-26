from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.html import format_html
from .models import TelegramUser

def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Mark selected as active"
class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = staticfiles_storage.url('core/static/core/css/admin.css')
        return context

admin_site = CustomAdminSite(name='custom_admin')

@admin.register(TelegramUser, site=admin_site)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'user', 'chat_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('telegram_username', 'user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'telegram_username', 'chat_id')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )