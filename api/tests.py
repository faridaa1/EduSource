from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from api.models import User

TEST_EMAIL = 'farida@gmail.com'
TEST_FIRST_NAME = 'farida'
TEST_LAST_NAME = 'adiraf'
TEST_PHONE_NUMBER = '0711111111'
TEST_USERNAME = 'farida'
TEST_PASSWORD = 'farida123'
TEST_THEME = 'dark'
TEST_MODE = 'seller'
TEST_DESCRIPTION = 'A new seller selling things which can be sold.'
TEST_ADDRESS_FIRST_LINE = '4 Maple Avenue'
TEST_ADDRESS_SECOND_LINE = 'Hillside Road'
TEST_CITY = 'London'
TEST_POSTCODE = 'E12QE'

class UnitTesting(TestCase):
    """Comprehensive unit testing"""
    def setUp(self):
        self.client = Client()
        # user = User.objects.create(username=TEST_USERNAME)
        # user.set_password(TEST_PASSWORD)
        # user.save()
    
    def test_valid_signup(self):
        # Beginning of code taken from ECS639U socialnetwork_v2 folder
        url = reverse('api:signup') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'email': TEST_EMAIL,
            'first_name': TEST_FIRST_NAME,
            'last_name': TEST_LAST_NAME,
            'phone_number': TEST_PHONE_NUMBER,
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
            'reenter_password': TEST_PASSWORD,
            'theme_preference': TEST_THEME,
            'mode': TEST_MODE,
            'description': TEST_DESCRIPTION,
            'first_line': TEST_ADDRESS_FIRST_LINE,
            'second_line': TEST_ADDRESS_SECOND_LINE,
            'city': TEST_CITY,
            'postcode': TEST_POSTCODE,
        }, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/details')
    
    def test_invalid_signup(self):
        # Beginning of code taken from ECS639U socialnetwork_v2 folder
        url = reverse('api:signup') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'email': 'a',
            'first_name': '@',
            'last_name': '@',
            'phone_number': ']',
            'username': '#',
            'password': 'o',
            'reenter_password': 'l',
            'theme_preference': TEST_THEME,
            'mode': TEST_MODE,
            'description': 'more than  one spaces  between',
            'first_line': '',
            'second_line': '',
            'city': '',
            'postcode': 'toomanycharacters',
        }, follow=True)
        print(response.context['signup_form'].errors)
        print(response.context['address_form'].errors)
        # self.assertEqual(response.request['PATH_INFO'], '/signup')



# class FunctionalTesting(StaticLiveServerTestCase):
#     """Functional testing in Selenium"""
#     port = 8000

#     @classmethod
#     def setUpClass(cls):
#         cls.selenium = WebDriver()
#         super().setUpClass()
    
#     # @classmethod
#     # def tearDownClass(cls):
#     #     cls.selenium.quit()
#     #     super().tearDownClass()
    
#     def get_url(self, path):
#         """Function to retrieve url given a path"""
#         self.selenium.get(f"{self.live_server_url}/{path}/")
#     def test_edusource(self):
#         """Combine individual methods"""
#         self.test_signup()
    
#     def test_signup(self):
#         """Testing signup"""

#         # Retrieve url
#         self.get_url('signup')

#         # Fill in fields
#         email_field = self.selenium.find_element(By.ID, 'email')
#         email_field.click()
#         email_field.send_keys(TEST_EMAIL)
