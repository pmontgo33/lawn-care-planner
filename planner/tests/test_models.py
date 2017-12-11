"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from django.test import TestCase
from planner.models import Lawn, GrassType, LawnProduct, WeatherStation
from django.contrib.auth.models import User

from datetime import date


class ModelTestCase(TestCase):

    def test_saving_and_retrieving_lawns(self):

        test_user = User()
        test_user.save()

        test_grass = GrassType()
        test_grass.name = 'Kentucky Bluegrass'
        test_grass.season = "Cool Season"
        test_grass.save()

        first_lawn = Lawn()
        first_lawn.user_id = 1
        first_lawn.name = "First Lawn"
        first_lawn.zip_code = "19075"
        first_lawn.size = 3000
        first_lawn.grass_type = test_grass
        first_lawn.save()

        second_lawn = Lawn()
        second_lawn.user_id = 1
        second_lawn.name = "Second Lawn"
        second_lawn.zip_code = "10314"
        second_lawn.size = 4500
        second_lawn.grass_type = test_grass
        second_lawn.save()

        saved_items = Lawn.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_lawn = saved_items[0]
        second_saved_lawn = saved_items[1]
        self.assertEqual(first_saved_lawn.name, "First Lawn")
        self.assertEqual(second_saved_lawn.name, "Second Lawn")

    def test_saving_and_retrieving_lawnproducts(self):

        seed_product = LawnProduct()
        seed_product.type = "Grass Seed"
        seed_product.name = "Monty's KBG"
        seed_product.links = {
            'LCP', 'www.lawncareplanner.com'
        }
        seed_product.specs = {
          "type":"Kentucky Bluegrass",
          "coated":False
        }
        seed_product.save()

        fert_product = LawnProduct()
        fert_product.type = "Fertilizer"
        fert_product.name = "Monty's Great Fert"
        fert_product.links = {
            'LCP', 'www.lawncareplanner.com'
        }
        fert_product.specs = {
          "organic":True,
          "npk":[5,2,0]
        }
        fert_product.save()

        self.assertEqual(LawnProduct.objects.count(), 2)

        saved_seed = LawnProduct.objects.filter(type='Grass Seed')[0]
        saved_fert = LawnProduct.objects.filter(type='Fertilizer')[0]
        self.assertEqual(saved_seed.name, "Monty's KBG")
        self.assertEqual(saved_fert.name, "Monty's Great Fert")

    def test_saving_and_retrieving_weatherstation(self):

        first_station = WeatherStation()
        first_station.name = "STATION IN ORELAND"
        first_station.stationid = 88
        first_station.latitude = 40.1148
        first_station.longitude = -75.1873
        first_station.datacoverage = 1
        first_station.elevation = 7.0
        first_station.elevationUnit = "METERS"
        first_station.maxdate = date(year=2010, month=12, day=31)
        first_station.mindate = date(year=2010, month=1, day=1)
        first_station.temp_data = {
          "2010-01-14":{
            "TMAX":83.2,
            "TMIN":74.2
          },
          "2010-11-16":{
            "TMAX":85.9,
            "TMIN":76.7
          }
        }
        first_station.save()

        second_station = WeatherStation()
        second_station.name = "STATION IN STATEN ISLAND"
        second_station.stationid = 66
        second_station.latitude = 40.6311
        second_station.longitude = -74.1364
        second_station.datacoverage = 1
        second_station.elevation = 12.0
        second_station.elevationUnit = "METERS"
        second_station.maxdate = date(year=2010, month=12, day=31)
        second_station.mindate = date(year=2010, month=1, day=1)
        second_station.temp_data = {
            "2010-10-07":{
            "TMAX":88.6,
            "TMIN":78.1
          },
          "2010-10-15":{
            "TMAX":88.1,
            "TMIN":77.9
          }
        }
        second_station.save()

        self.assertEqual(WeatherStation.objects.count(), 2)

        first_saved_station = WeatherStation.objects.get(pk=88)
        second_saved_station = WeatherStation.objects.get(pk=66)
        self.assertEqual(first_saved_station.name, "STATION IN ORELAND")
        self.assertEqual(second_saved_station.name, "STATION IN STATEN ISLAND")