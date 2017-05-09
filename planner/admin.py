"""
This file creates custom admin sections for models, and registers models on the admin site.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from planner.models import Lawn, WeatherStation, LawnProduct, GrassType


UserAdmin.list_display = ['email', 'first_name', 'last_name', 'is_staff']


class LawnAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_email', 'zip_code', 'grass_type', 'size', 'weekly_notify']
    search_fields = ['user__email']

    def user_email(self, obj):
        return str(obj.user.email)
    user_email.admin_order_field = 'user__email'


class LawnProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ('type',)


class GrassTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'season']
    list_filter = ('season',)


class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'stationid', 'latitude', 'longitude']
    search_fields = ['name']


admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(Lawn, LawnAdmin)
admin.site.register(LawnProduct, LawnProductAdmin)
admin.site.register(GrassType, GrassTypeAdmin)
