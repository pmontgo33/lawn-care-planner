"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from django.test import TestCase


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