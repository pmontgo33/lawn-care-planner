"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from django.test import TestCase
from planner.models import Lawn, GrassType, LawnProduct
from django.contrib.auth.models import User


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
