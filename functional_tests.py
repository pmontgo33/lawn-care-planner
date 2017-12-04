from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_navagate_to_new_lawn_and_create_planner(self):
        # User finds LCP site. User goes to homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

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
        time.sleep(1)

        lawn_name = self.browser.find_element_by_id("id_lawn_name").text
        self.assertIn("Lawn Name: ", lawn_name)

        weather_station = self.browser.find_element_by_id("id_weather_station").text
        self.assertIn("Closest Weather Station: ", weather_station)

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()