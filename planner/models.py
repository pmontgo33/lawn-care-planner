# planner/models.py
# Patrick W. Montgomery
# created: 10/9/2016

from django.db import models
from planner.lawn import seeding, lawnutils
from jsonfield import JSONField

import os
import json
import collections


class Lawn(models.Model):
    """
    The Lawn model contains all of the properties for a specific lawn.
    """
    user = models.ForeignKey('auth.user')
    name = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=5)
    grass_type = models.ForeignKey('GrassType')
    size = models.IntegerField()
    
    def __str__(self):
        return self.name


class WeatherStation(models.Model):
    """
    This model is used to store the temperature data for each weather station
    """
    name = models.CharField(max_length=200)
    stationid = models.CharField(max_length=200, primary_key=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    datacoverage = models.IntegerField(default=0)
    elevation = models.FloatField(default=0.0)
    elevationUnit = models.CharField(max_length=200)
    maxdate = models.DateField()
    mindate = models.DateField()
    temp_data = JSONField()
    
    def __str__(self):
        return self.name
   
    @staticmethod    
    def load_stations_to_database():
    
        """
        This function reads the already downloaded Daily Normal Temperature data for 
        all available stations, and loads it into the Django database.
        """
        
        file_dir = os.path.dirname(os.path.realpath(__file__)) + "/code/FullNormalTempData.dat"
        temp_data_file = open(file_dir, "r")
        temp_data_file.readline() # file title
        temp_data_file.readline() # [
        
        LINES_IN_STATION = 11 + 4*365 + 2 # 11 gets you up to openning temp_data. each temp date is 4 lines * 365 days. 2 closes brackets.
        BATCH_SIZE = 30
        
        #    [print(i,temp_data_file.readline()) for i in range(11 + 4*365 + 2)]
        
        def station_json_generator():
            for i in range(BATCH_SIZE):
                station_json = "".join([temp_data_file.readline() for x in range(LINES_IN_STATION)])
                if len(station_json) <= 2: # this means its not a station.
                    yield ""
                if station_json[-2] == ",":
                    station_json = station_json[:-2] # remove the comma at the end
                yield station_json
        
        eof = False
        while not eof:
            stations_batch = []
            for station_json in station_json_generator():
                if station_json == "":
                    eof = True
                    break
                stations_batch.append(json.loads(station_json))

            stations_to_add = []
            for station in stations_batch:
                WeatherStation.objects.update_or_create(
                    stationid=station['id'],
                    defaults = {
                        'name': station['name'],
                        'latitude': station['latitude'],
                        'longitude': station['longitude'],
                        'datacoverage': station['datacoverage'],
                        'elevation': station['elevation'],
                        'elevationUnit': station['elevationUnit'],
                        'maxdate': station['maxdate'],
                        'mindate': station['mindate'],
                        'temp_data': station['temp_data']
                    }
                )
        
        temp_data_file.close()


class LawnProduct(models.Model):

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=140, choices=(
        ("Grass Seed", "Grass Seed"),
        ("Fertilizer", "Fertilizer"),
        ("Weed Control", "Weed Control"),
        ("Insect Control", "Insect Control")
    ))
    links = JSONField()
    specs = JSONField()

    class Meta:
        ordering = ['type', 'name']

    def __str__(self):
        return "%s - %s" % (self.type,self.name)


class GrassType(models.Model):

    name = models.CharField(max_length=200)
    season = models.CharField(choices=(("Cool Season", "Cool Season"), ("Warm Season", "Warm Season")), max_length=200)
    seed = models.BooleanField(default=True)
    plugs = models.BooleanField(default=False)
    mowing = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    specs = JSONField()

    def __str__(self):
        return self.name