from selenium.webdriver.support.ui import Select
from unittest import skip
from .base import FunctionalTest

import time


class LawnValidationTest(FunctionalTest):

    def test_cannot_submit_lawn_with_invalid_zip_code(self):
        # User visits LCP homepage
        self.browser.get(self.live_server_url)

        # User clicks on planner link in banner
        self.browser.find_element_by_link_text("Planner").click()
        self.wait_for(lambda: self.assertIn(
            'id_zip_code',
            self.browser.find_element_by_id('id_zip_code').get_attribute('id')
        ))

        # Users enters an invalid zip code, but a selects a valid grass type, and enters a valid size
        uls = self.browser.find_elements_by_tag_name('ul')
        self.assertNotIn('errorlist', [ul.get_attribute('class') for ul in uls])
        zip_input = self.browser.find_element_by_id('id_zip_code')
        zip_input.send_keys('55555')

        type_input = Select(self.browser.find_element_by_id('id_grass_type'))
        type_input.select_by_visible_text('Perennial Ryegrass')

        size_input = self.browser.find_element_by_id('id_size')
        size_input.send_keys('5000')

        # When user presses clicks submit, he sees an error message
        self.browser.find_element_by_class_name("save").click()
        self.wait_for_class_in_element_list('errorlist', self.browser.find_elements_by_tag_name('ul'))

        # User changes zip code to a valid zip code, and clicks submit again
        zip_input = self.browser.find_element_by_id('id_zip_code')
        zip_input.clear()
        zip_input.send_keys('60652')
        self.browser.find_element_by_class_name("save").click()
        self.wait_for_element('id_lawn_name')

        # User is taken to a page that displays his lawn planner for the year
        lawn_name = self.browser.find_element_by_id('id_lawn_name').text
        self.assertIn('Lawn Name: ', lawn_name)

        weather_station = self.browser.find_element_by_id('id_weather_station').text
        self.assertIn('Closest Weather Station: ', weather_station)