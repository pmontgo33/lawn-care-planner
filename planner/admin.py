"""
This file creates custom admin sections for models, and registers models on the admin site.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from planner.models import Lawn, WeatherStation, LawnProduct, GrassType


UserAdmin.list_display = ['email', 'first_name', 'last_name', 'is_staff']


class LawnAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_email', 'zip_code', 'grass_type', 'size', 'weekly_notify']
    search_fields = ['user__email']

    def user_email(self, obj):
        return str(obj.user.email)
    user_email.admin_order_field = 'user__email'

class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'stationid', 'latitude', 'longitude']
    search_fields = ['name']

admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(Lawn, LawnAdmin )
admin.site.register(LawnProduct)
admin.site.register(GrassType)
