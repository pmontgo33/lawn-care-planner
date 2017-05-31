# planner/models.py
# Patrick W. Montgomery
# created: 10/9/2016

from django.db import models
from django.core.urlresolvers import reverse
from jsonfield import JSONField

import os
import json
import collections

from planner.lawn import lawnutils

import logging
logger = logging.getLogger(__name__)


class Lawn(models.Model):
    """
    The Lawn model contains all of the properties for a specific lawn.
    """

    # Basic fields
    user = models.ForeignKey('auth.user')
    name = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=5)
    grass_type = models.ForeignKey('GrassType')
    size = models.IntegerField()
    weekly_notify = models.BooleanField(default=True)

    # Optional fields
    spring_seeding = models.BooleanField(default=False)
    organic = models.CharField(default='NP', max_length=2)

    # Advanced fields
    advanced = models.BooleanField(default=False)
    phosphorus = models.PositiveSmallIntegerField(default=0)

    @property
    def seed_new_lb_range(self):
        if not self.grass_type.seed:
            return None
        return [lawnutils.round_to_quarter(x * (self.size / 1000)) for x in
                self.grass_type.specs['seed_new_lb_range']]

    @property
    def seed_over_lb_range(self):
        if not self.grass_type.seed:
            return None
        return [lawnutils.round_to_quarter(x * (self.size / 1000)) for x in
                self.grass_type.specs['seed_over_lb_range']]

    @property
    def number_of_plugs(self):
        if not self.grass_type.plugs:
            return None

        PLUGS_PER_SF = .5625
        return round(PLUGS_PER_SF * self.size)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lawn_detail', kwargs={'pk':self.pk})


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
    temp_data = JSONField(default="{}")
    
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

    class Meta:
        ordering = ['season','name']

    def __str__(self):
        return self.name