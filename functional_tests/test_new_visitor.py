from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

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
        self.wait_for(lambda: self.assertIn(
            'Lawn Name: ',
            self.browser.find_element_by_id('id_lawn_name').text
        ))

        weather_station = self.browser.find_element_by_id('id_weather_station').text
        self.assertIn('Closest Weather Station: ', weather_station)

    def test_examples_can_load(self):
        # User visits LCP homepage
        self.browser.get(self.live_server_url)

        # User decides to check out the available examples, and clicks on the Examples button in the banner
        self.browser.find_element_by_link_text("Examples").click()
        self.wait_for(lambda: self.assertIn(
            'Create a Lawn',
            self.browser.find_element_by_id('id_create_lawn').text
        ))

        # User sees a list of example lawns
        lawns = self.browser.find_elements_by_tag_name('h5')
        self.assertGreater(len(lawns), 2)

        # User clicks an example lawn, and is taken to the detail page
        self.browser.find_element_by_link_text(lawns[0].text).click()
        self.wait_for(lambda: self.assertIn(
            'Lawn Name: ',
            self.browser.find_element_by_id('id_lawn_name').text
        ))

        # User clicks the back button, and again sees the list of example lawns
        self.browser.back()
        self.wait_for(lambda: self.assertIn(
            'Create a Lawn',
            self.browser.find_element_by_id('id_create_lawn').text
        ))

        # User selects a different example lawn, and is taken to the detail page
        lawns = self.browser.find_elements_by_tag_name('h5')
        self.browser.find_element_by_link_text(lawns[1].text).click()
        self.wait_for(lambda: self.assertIn(
            'Lawn Name: ',
            self.browser.find_element_by_id('id_lawn_name').text
        ))