"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from django.test import TestCase
from planner.models import Lawn, GrassType
from django.contrib.auth.models import User
from django.urls import resolve
from planner.views import index


class ModelTestCase(TestCase):

    def test_saving_and_retrieving_lawns(self):

        test_user = User()
        test_user.save()

        test_grass = GrassType()
        test_grass.name = 'Kentucky Bluegrass'
        test_grass.season = ("Cool Season", "Cool Season")
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


class IndexTest(TestCase):

    def test_index_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/index.html')


class NewLawnTest(TestCase):

    def test_new_lawn_loads(self):
        response = self.client.get('/planner/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/lawn_edit.html')
# class PlannerViewsTestCase(TestCase):
#     fixtures = ['planner_views_testdata.json', 'auth_views_testdata.json']
#
#     def test_detail(self):
#         """
#         test if lawn detail page loads.
#         :return:
#         """
#         resp = self.client.get('/planner/lawn/1/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(resp.context['lawn'].pk, 1)
#         self.assertEqual(resp.context['lawn'].name, "ORELAND PA Lawn")
#
#         # Ensure that non-existent lawns throw a 404
#         resp = self.client.get('planner/lawn/3333/')
#         self.assertEqual(resp.status_code, 404)