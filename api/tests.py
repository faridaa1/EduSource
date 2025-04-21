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
    
    def test_invalid_format_signup(self):
        """Testing when input is in invalid format"""
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
            'description': 'two  spaces',
            'first_line': 'two  spaces',
            'second_line': 'two  spaces',
            'city': 'two  spaces',
            'postcode': 'toomanycharacters',
        }, follow=True)
        self.assertContains(response, 'Enter a valid email address')
        self.assertEqual(response.content.decode().count('Only letters are allowed'), 2)
        self.assertContains(response, 'Username cannot contain special characters')
        self.assertContains(response, 'Must be 10 or 11 digit number starting with 07')
        self.assertContains(response, 'Username cannot contain special characters')
        self.assertContains(response, 'Password must be between 8 to 15 characters long')
        self.assertEqual(response.content.decode().count('Only one space between words'), 4)
        self.assertContains(response, 'Ensure this value has at most 7 characters')
        self.assertEqual(response.request['PATH_INFO'], '/signup/') # Ensure no page redirect

        # Trying where first name and last name have two spaces between words
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'email': TEST_EMAIL,
            'first_name': 'invalid  input',
            'last_name': 'invalid  input',
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
        self.assertEqual(response.content.decode().count('Only one space between words'), 2)
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_empty_inputs_signup(self):
        url = reverse('api:signup') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'email': '',
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'username': '',
            'password': '',
            'reenter_password': '',
            'theme_preference': 'light', # Default value
            'mode': 'seller', # Seller added to ensure description field is visible
            'description': '',
            'first_line': '',
            'second_line': '',
            'city': '',
            'postcode': '',
        }, follow=True)

        self.assertEqual(response.content.decode().count('This field is required'), 11)
        self.assertEqual(response.request['PATH_INFO'], '/signup/')

    def test_existing_username_signup(self):
        # Creating existing user
        user = User.objects.create(username=TEST_USERNAME)
        user.set_password(TEST_PASSWORD)
        user.save()

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

        self.assertContains(response, 'A user with that username already exists')
        self.assertEqual(response.request['PATH_INFO'], '/signup/')

    def test_existing_email_signup(self):
        # Creating existing user
        user = User.objects.create(username='test123')
        user.set_password(TEST_PASSWORD)
        user.email = TEST_EMAIL
        user.save()

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

        self.assertContains(response, 'User with this Email already exists')
        # print(response.context['signup_form'].errors)
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_existing_number_signup(self):
        # Creating existing user
        user = User.objects.create(username='test123')
        user.set_password(TEST_PASSWORD)
        user.phone_number = TEST_PHONE_NUMBER
        user.save()

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

        self.assertContains(response, 'User with this Phone number already exists')
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_mismatched_password_signup(self):
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
            'reenter_password': TEST_PASSWORD+'1',
            'theme_preference': TEST_THEME,
            'mode': TEST_MODE,
            'description': TEST_DESCRIPTION,
            'first_line': TEST_ADDRESS_FIRST_LINE,
            'second_line': TEST_ADDRESS_SECOND_LINE,
            'city': TEST_CITY,
            'postcode': TEST_POSTCODE,
        }, follow=True)

        self.assertContains(response, 'Both passwords must match')
        # print(response.context['signup_form'].errors)
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_valid_login(self):
        # Creating existing user
        user = User.objects.create(username=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }, follow=True)
        print(response.request['PATH_INFO'])
        # self.assertEqual(response.request['PATH_INFO'], '/details')

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
    
#     def test_signup(self):
#         """Testing signup"""
#         # Retrieve url
#         self.get_url('signup')

#         # Fill in fields
#         email_field = self.selenium.find_element(By.NAME, 'email')
#         email_field.click() # Simulate user clicking input box
#         email_field.send_keys(TEST_EMAIL)

#         first_name_field = self.selenium.find_element(By.NAME, 'first_name')
#         first_name_field.click()
#         first_name_field.send_keys(TEST_FIRST_NAME)

#         last_name_field = self.selenium.find_element(By.NAME, 'last_name')
#         last_name_field.click()
#         last_name_field.send_keys(TEST_LAST_NAME)

#         phone_number_field = self.selenium.find_element(By.NAME, 'phone_number')
#         phone_number_field.click()
#         phone_number_field.send_keys(TEST_PHONE_NUMBER)

#         username_field = self.selenium.find_element(By.NAME, 'username')
#         username_field.click()
#         username_field.send_keys(TEST_USERNAME)

#         password_field = self.selenium.find_element(By.NAME, 'password')
#         password_field.click()
#         password_field.send_keys(TEST_PASSWORD)

#         reenter_password_field = self.selenium.find_element(By.NAME, 'reenter_password')
#         reenter_password_field.click()
#         reenter_password_field.send_keys(TEST_PASSWORD)

#         last_name_field = self.selenium.find_element(By.NAME, 'last_name')
#         last_name_field.click()
#         last_name_field.send_keys(TEST_LAST_NAME)

#         theme_field = self.selenium.find_element(By.NAME, 'theme_preference')
#         theme_field.click()
#         dark_option = self.selenium.find_element(By.XPATH, "//option[@value='dark']")
#         dark_option.click()

#         mode_field = self.selenium.find_element(By.NAME, 'mode')
#         mode_field.click()
#         seller_option = self.selenium.find_element(By.XPATH, "//option[@value='seller']")
#         seller_option.click()

#         description_field = self.selenium.find_element(By.NAME, 'description')
#         description_field.click()
#         description_field.send_keys(TEST_DESCRIPTION)

#         first_line_field = self.selenium.find_element(By.NAME, 'first_line')
#         first_line_field.click()
#         first_line_field.send_keys(TEST_ADDRESS_FIRST_LINE)

#         second_line_field = self.selenium.find_element(By.NAME, 'second_line')
#         second_line_field.click()
#         second_line_field.send_keys(TEST_ADDRESS_SECOND_LINE)

#         city_field = self.selenium.find_element(By.NAME, 'city')
#         city_field.click()
#         city_field.send_keys(TEST_CITY)

#         postcode_field = self.selenium.find_element(By.NAME, 'postcode')
#         postcode_field.click()
#         postcode_field.send_keys(TEST_POSTCODE)

#         # Submit form
#         submit_button = self.selenium.find_element(By.ID, 'submit')
#         submit_button.click()