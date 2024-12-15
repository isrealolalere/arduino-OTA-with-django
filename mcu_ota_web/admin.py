from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_key', 'phone_no')
    search_fields = ('user__username', 'device_key')


@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('user_device', 'version', 'release_date')
    list_filter = ('release_date', 'user_device')
    search_fields = ('user_device__user__username', 'version')
    ordering = ('-release_date',)

    def user_device_username(self, obj):
        return obj.user_device.user.username
    user_device_username.short_description = 'User Device Username'