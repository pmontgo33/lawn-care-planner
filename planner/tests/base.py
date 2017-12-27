from django.test import TestCase


class UnitTestWithFixtures(TestCase):
    fixtures = ['auth_views_testdata.json', 'planner_grasstype_testdata.json', 'planner_lawn_testdata.json',
                'planner_lawnproduct_testdata.json', 'planner_weatherstation_testdata.json']