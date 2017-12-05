from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import os
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

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

    def test_can_navigate_to_new_lawn_and_create_planner(self):
        # User finds LCP site. User goes to homepage
        self.browser.get(self.live_server_url)

        # User can see the page title and notices header mention LCP
        self.assertIn('Lawn Care Planner', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Lawn Care Planner', header_text)

        # User sees a link to create a new planner for his lawn
        planner_btn = self.browser.find_element_by_id('id_create_planner')
        planner_url = self.browser.current_url + 'planner'
        self.assertEqual(planner_btn.get_attribute('href'), planner_url)

        # User clicks link, and loads a page titled Create Lawn
        self.browser.find_element_by_id('id_create_planner').click()
        self.wait_for_element('id_zip_code')

        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Create Lawn', header_text)

        # User sees labels for inputting zip code, grass type, and lawn size
        labels = self.browser.find_elements_by_tag_name('label')

        self.assertIn('id_zip_code', [label.get_attribute('for') for label in labels])
        self.assertIn('id_grass_type', [label.get_attribute('for') for label in labels])
        self.assertIn('id_size', [label.get_attribute('for') for label in labels])

        # User enters his zip code, selects grass type from dropdown, types in lawn size, and clicks ENTER
        zip_input = self.browser.find_element_by_id('id_zip_code')
        zip_input.send_keys('19075')

        type_input = Select(self.browser.find_element_by_id('id_grass_type'))
        type_input.select_by_visible_text('Kentucky Bluegrass')

        size_input = self.browser.find_element_by_id('id_size')
        size_input.send_keys('3000')

        # When user presses enter, he is taken to a page that displays his lawn planner for the year
        size_input.send_keys(Keys.ENTER)
        self.wait_for_element('id_lawn_name')

        lawn_name = self.browser.find_element_by_id('id_lawn_name').text
        self.assertIn('Lawn Name: ', lawn_name)

        weather_station = self.browser.find_element_by_id('id_weather_station').text
        self.assertIn('Closest Weather Station: ', weather_station)
