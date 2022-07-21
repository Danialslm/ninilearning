from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Device


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'vip_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active', 'is_vip')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)

    @admin.display(description=_('vip'), boolean=True)
    def is_vip(self, obj):
        return obj.is_vip


@admin.register(Device)
class DevicesAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'ip_address')
