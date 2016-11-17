# planner/admin.py
# Patrick W. Montgomery
# created: 10/9/2016

from django.contrib import admin
from planner.models import Lawn, WeatherStation

admin.site.register(Lawn)
admin.site.register(WeatherStation)

"""
"datacoverage": 1,
        "elevation": 3.7,
        "elevationUnit": "METERS",
        "id": "GHCND:AQW00061705",
        "latitude": -14.33056,
        "longitude": -170.71361,
        "maxdate": "2010-12-31",
        "mindate": "2010-01-01",
        "name": "PAGO PAGO WEATHER SERVICE OFFICE AIRPORT, US",
"""