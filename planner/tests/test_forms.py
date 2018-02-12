from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from unittest import skip

from planner.forms import LawnForm
from planner.models import GrassType
from .base import UnitTestWithFixtures

import logging
logger = logging.getLogger(__name__)


class LawnFormTest(TestCase):

    def test_form_renders_lawn_text_input_when_authenticated(self):
        test_user = User(username='newtestuser', password='test', pk=1)
        test_user.save()
        test_user.full_clean()

        form = LawnForm(test_user)
        self.assertIn('id="id_name"', form.as_p())
        self.assertIn('id="id_zip_code"', form.as_p())
        self.assertIn('id="id_grass_type"', form.as_p())
        self.assertIn('id="id_size"', form.as_p())
        self.assertIn('id="id_weekly_notify"', form.as_p())

    def test_form_renders_lawn_text_input_when_anonymous(self):
        test_user = AnonymousUser()

        form = LawnForm(test_user)
        self.assertNotIn('id="id_name"', form.as_p())
        self.assertNotIn('id="id_weekly_notify"', form.as_p())
        self.assertIn('id="id_zip_code"', form.as_p())
        self.assertIn('id="id_grass_type"', form.as_p())
        self.assertIn('id="id_size"', form.as_p())

    def test_form_validation_for_blank_items(self):
        test_user = AnonymousUser()

        form = LawnForm(test_user, data={'zip_code': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['zip_code'], ['This field is required.'])

    def test_form_validation_for_invalid_items(self):
        test_user = AnonymousUser()

        form = LawnForm(test_user, data={'zip_code': '55555'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['zip_code'], ['Invalid ZIP code'])

    def test_new_lawn_page_uses_form_instance(self):
        response = self.client.get('/planner/')
        self.assertIsInstance(response.context['form'], LawnForm)


class LawnFormTestWithFixtures(UnitTestWithFixtures):

    def test_form_valid_with_basic_planner(self):
        test_user = AnonymousUser()

        form_data = {'name': 'Basic Lawn', 'zip_code': '18914', 'grass_type': 2, 'size': 4000,
                     'advanced': False, 'organic': 'NP'}

        form = LawnForm(test_user, data=form_data)
        self.assertTrue(form.is_valid(), msg='Form errors: %s' % form.errors)

    def test_form_valid_with_advanced_planner(self):
        test_user = AnonymousUser()

        form_data = {'name': 'Basic Lawn', 'zip_code': '18914', 'grass_type': 2, 'size': 4000,
                     'advanced': False, 'organic': 'NP', 'weekly_notify': False, 'lime': '0', 'phosphorus': '0',
                     'potassium': '0'}

        form = LawnForm(test_user, data=form_data)

        self.assertTrue(form.is_valid(), msg='Form errors: %s' % form.errors)

    def test_edit_lawn_page_uses_form_instance(self):
        self.client.login(username='test', password='testpassword')
        response = self.client.get('/planner/lawn/6/edit/')
        self.assertIsInstance(response.context['form'], LawnForm)
