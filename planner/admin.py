# planner/admin.py
# Patrick W. Montgomery
# created: 10/9/2016

from django.contrib import admin
from planner.models import Lawn, WeatherStation


class WeatherStationAdmin(admin.ModelAdmin):
       list_display = ['name', 'stationid', 'latitude', 'longitude']
       search_fields = ['name']
        
admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(Lawn)