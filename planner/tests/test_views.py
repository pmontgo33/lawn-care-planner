"""
This file contains all of the unit tests for the planner django app
"""

# Import Statements
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