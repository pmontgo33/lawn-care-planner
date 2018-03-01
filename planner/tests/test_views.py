"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
from datetime import timedelta
from django.test import TestCase
from django.contrib import auth
from unittest import skip

from .base import UnitTestWithFixtures
from planner.forms import LawnForm

import logging
logger = logging.getLogger(__name__)


class IndexViewTest(TestCase):

    def test_index_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/index.html')


class LawnDetailTest(UnitTestWithFixtures):

    def test_lawn_detail_view(self):
        response = self.client.get('/planner/lawn/4/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lawn'].pk, 4)
        self.assertEqual(response.context['lawn'].name, "Lawn 19075")

    def test_invalid_throws_error(self):
        response = self.client.get('planner/lawn/3333/')
        self.assertEqual(response.status_code, 404)

    def test_advanced_lawn_detail_view(self):
        response = self.client.get('/planner/lawn/14/')
        self.assertEqual(response.status_code, 200)

        phlime_apps = response.context['planner'].phlime_info['apps']
        fert_apps = response.context['planner'].fertilizer_info['apps']
        has_lime = False
        has_phosphorus = False
        has_potassium = False

        for season, apps in phlime_apps.items():
            for app in apps:
                if app['nutrient'] == 'Lime':
                    has_lime = True
        self.assertTrue(has_lime, msg="Lime application not present.")

        for season, apps in fert_apps.items():
            for app in apps:
                if app['nutrient'] == 'Phosphorus':
                    has_phosphorus = True
        self.assertTrue(has_phosphorus, msg="Phosphorus application not present.")
        # self.assertTrue(has_potassium, msg="Potassium application not present.")

    def check_lime_constraints(self, phlime_apps, fert_apps, expected_apps):
        """
        Lime Constraints

        - Number of applications - According to PSU soil test results, lime applications should be spaced out by 4-6
            months (at least 120 days between) , and therefore should not have more than 2 applications per year.
        - Application rate - According to PSU soil test results, lime applications should not exceed 100 lbs per 1000sf.
            Other sources, such as U of Arkansas (https://www.uaex.edu/publications/PDF/FSA-6134.pdf) recommend not
            exceeding 50lbs per 1000sf per application. LCP has gone with the more conservative rate of 50lb/1000sf
        """
        lime_apps = []
        for season, apps in phlime_apps.items():
            for app in apps:
                if app['nutrient'] == 'Lime':
                    lime_apps.append(app)
        nitrogen_apps = []
        for season, apps in fert_apps.items():
            for app in apps:
                if app['nutrient'] == 'Lime':
                    lime_apps.append(app)

        self.assertTrue(len(lime_apps) <= 2,
                        msg="Lime applications: %s. Lime applications cannot exceed 2." % len(lime_apps))
        for app in lime_apps:
            for another in lime_apps:
                if app == another:
                    continue
                days_between = abs(app['date'] - another['date']).days
                self.assertTrue(days_between > 120,
                                msg="Days between lime applications %s. Must be more than 120 days." % days_between)
            for n_app in nitrogen_apps:
                days_between = abs(app['date'] - n_app['date']).days
                self.assertTrue(days_between > 14,
                                msg="Days between nitrogen and lime applications %s. Must be more than 14 days." % days_between)
            self.assertTrue(app['rate'] <= 50, msg="Lime app rate: %s. Lime app rates cannot exceed 50." % app['rate'])

        self.assertTrue(len(lime_apps) == expected_apps, msg="Expected %s lime application, found %s" %
                        (expected_apps, len(lime_apps)))

    def test_advanced_lawn_lime_one_app(self):

        response = self.client.get('/planner/lawn/15/')
        self.assertEqual(response.status_code, 200)

        fert_apps = response.context['planner'].fertilizer_info['apps']
        phlime_apps = response.context['planner'].phlime_info['apps']
        expected_apps = 1
        self.check_lime_constraints(phlime_apps, fert_apps, expected_apps)

    def test_advanced_lawn_lime_two_apps(self):

        response = self.client.get('/planner/lawn/16/')
        self.assertEqual(response.status_code, 200)

        fert_apps = response.context['planner'].fertilizer_info['apps']
        phlime_apps = response.context['planner'].phlime_info['apps']
        expected_apps = 2
        self.check_lime_constraints(phlime_apps, fert_apps, expected_apps)

    def test_advanced_lawn_lime_more_than_two_apps(self):

        response = self.client.get('/planner/lawn/17/')
        self.assertEqual(response.status_code, 200)

        fert_apps = response.context['planner'].fertilizer_info['apps']
        phlime_apps = response.context['planner'].phlime_info['apps']
        expected_apps = 2
        self.check_lime_constraints(phlime_apps, fert_apps, expected_apps)

    def test_advanced_lawn_phosphorus_constraints_pass(self):
        # Phosphorus Constraints
        self.fail("Finish the phosphorus constraints")

    def test_advanced_lawn_phosphorus_constraints_pass(self):
        # Potassium Constraints
        self.fail("Finish the potassium constraints")


class NewLawnViewTest(TestCase):

    def test_new_lawn_view_loads(self):
        response = self.client.get('/planner/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/lawn_edit.html')
        self.assertIsInstance(response.context['form'], LawnForm)


class UserLawnListViewTest(UnitTestWithFixtures):

    def test_user_lawn_list_view(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/planner/lawn/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/lawn_list.html')


class TestLawnDeleteView(UnitTestWithFixtures):

    def test_user_can_delete_his_own_lawn(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/planner/lawn/6/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/lawn_confirm_delete.html')

    def test_user_cannot_delete_his_own_lawn(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/planner/lawn/4/delete/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')


class TestLawnEditView(UnitTestWithFixtures):

    def test_user_can_edit_his_own_lawn(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/planner/lawn/6/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planner/lawn_edit.html')
        self.assertIsInstance(response.context['form'], LawnForm)

    def test_user_cannot_edit_his_own_lawn(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/planner/lawn/4/edit/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')


class ProfileUpdateAndDetailTest(UnitTestWithFixtures):

    def test_user_detail_loads_when_authenticated(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user_detail.html')

    def test_user_detail_redirects_when_anonymous(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/accounts/profile/')

    def test_profile_update_view_loads_when_authenticated(self):
        self.client.login(username="test", password='testpassword')
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'test')
        response = self.client.get('/accounts/profile/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_update_form.html')

    def test_profile_update_view_redirects_when_anonymous(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())
        response = self.client.get('/accounts/profile/edit/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/accounts/profile/edit/')