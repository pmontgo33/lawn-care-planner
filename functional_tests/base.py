from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import os
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    fixtures = ['auth_views_testdata.json', 'planner_grasstype_testdata.json', 'planner_lawn_testdata.json',
                'planner_lawnproduct_testdata.json', 'planner_weatherstation_testdata.json']

    def setUp(self):
        # os.environ['MOZ_HEADLESS'] = '1'
        # options = Options()
        # options.add_argument('--headless')
        # self.browser = webdriver.Firefox(firefox_options=options)
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_element(self, element_id):
        start_time = time.time()
        while True:
            try:
                element = self.browser.find_element_by_id(element_id)
                return
            except (NoSuchElementException, AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_class_in_element_list(self, class_att, element_list):
        start_time = time.time()
        while True:
            try:
                self.assertIn(class_att, [element.get_attribute('class') for element in element_list])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)