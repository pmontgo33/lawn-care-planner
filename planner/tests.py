"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from django.test import TestCase
from django.urls import resolve
from planner.views import index


class IndexTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'planner/index.html')


# class PlannerViewsTestCase(TestCase):
#     fixtures = ['planner_views_testdata.json', 'auth_views_testdata.json']
#
#     def test_index(self):
#         """
#         test if homepage (index) loads.
#         :return:
#         """
#         resp = self.client.get('/')
#         self.assertEqual(resp.status_code, 200)
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