from selenium import webdriver
import unittest


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
        self.fail('Finish the test!')

        # User sees a link to create a mew planner for his lawn

        # User clicks link, and loads a page that asks for zip code, grass type, and lawn size

        # User enters his zip code and lawn size

        # User clicks the dropdown for grass type, sees several options, and selects one

        # When user presses enter, he is taken to a page that displays his lawn planner for the year

if __name__ == '__main__':
    unittest.main()