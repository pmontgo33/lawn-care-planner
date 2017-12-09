from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import os
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    fixtures = ['auth_views_testdata.json', 'planner_grasstype_testdata.json', 'planner_lawn_testdata.json',
                'planner_lawnproduct_testdata.json', 'planner_weatherstation_testdata.json']

    def setUp(self):
        self.browser = webdriver.Chrome()
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
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)