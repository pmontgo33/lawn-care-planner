"""
This file contains all of the tests for the planner django app
"""

# Import Statements
from django.test import TestCase
from django.contrib.auth.models import User
from planner.models import Lawn, GrassType


class PlannerViewsTestCase(TestCase):

    def test_index(self):
        """
        test if homepage (index) loads.
        :return: 
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    #TODO: Add real tests
