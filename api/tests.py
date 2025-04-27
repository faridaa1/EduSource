from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

from api.models import Address, User

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
        # Creating user in database
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
        # Creating user in database
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
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_existing_number_signup(self):
        # Creating user in database
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
        self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    def test_valid_email_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }, follow=True)

        self.assertEqual(response.request['PATH_INFO'], '/')
    
    def test_valid_username_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }, follow=True)

        self.assertEqual(response.request['PATH_INFO'], '/')
    
    def test_valid_buyer_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL, mode='buyer')
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }, follow=True)

        self.assertEqual(response.request['PATH_INFO'], '/')
    
    def test_valid_seller_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL, mode='seller')
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/listings')
    
    def test_empty_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': '',
            'password': '',
        }, follow=True)

        self.assertEqual(response.content.decode().count('This field is required'), 2)
        self.assertEqual(response.request['PATH_INFO'], '/login/')
    
    def test_incorrect_password_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': TEST_EMAIL,
            'password': 'wrongpass123',
        }, follow=True)
        
        self.assertEqual(response.request['PATH_INFO'], '/login/')
        self.assertContains(response, 'Invalid email or password')

    def test_incorrect_username_login(self):
        # Creating user in database
        user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
        user.set_password(TEST_PASSWORD)
        user.save()

        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': 'wrongusername',
            'password': TEST_PASSWORD,
        }, follow=True)
        
        self.assertEqual(response.request['PATH_INFO'], '/login/')
        self.assertContains(response, 'Invalid username or password')
    
    def test_incorrect_login(self):
        url = reverse('api:login') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
        soup = BeautifulSoup(response.content, features="html.parser")
        csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
        response = self.client.post(url, {
            'csrfmiddlewaretoken': csrf_token['value'],
            'user': 'wrongusername',
            'password': 'wrongpass',
        }, follow=True)
        
        self.assertEqual(response.request['PATH_INFO'], '/login/')
        self.assertContains(response, 'Invalid username or password')
        # print(response.context['login_form'].errors)

class FunctionalTesting(StaticLiveServerTestCase):
    """Functional testing in Selenium"""
    port = 8000

    def setUp(self):
        # Ensure full screen is shown
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        self.selenium = WebDriver(options=options)
    
    def tearDown(self):
        self.selenium.quit()
    
    def get_url(self, path):
        """Function to retrieve url given a path"""
        self.selenium.get(f"{self.live_server_url}/{path}/")
    
    def buyer_login(self):
        """Method to log in user"""
        # Creating user in database
        user = User.objects.create(
            username=TEST_USERNAME, 
            email=TEST_EMAIL,
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            phone_number=TEST_PHONE_NUMBER,
            mode='buyer',
        )
        user.set_password(TEST_PASSWORD)
        user.save()
        address = Address.objects.create(
            first_line=TEST_ADDRESS_FIRST_LINE,
            second_line=TEST_ADDRESS_SECOND_LINE,
            city=TEST_CITY,
            postcode=TEST_POSTCODE,
            user=user
        )
        address.save()
        
        # Retrieve url
        self.get_url('login')

        # Fill in fields
        self.selenium.find_element(By.NAME, 'user').send_keys(TEST_USERNAME)
        self.selenium.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)

        # Submit form
        self.selenium.find_element(By.ID, 'submit').click()

    def seller_login(self):
        """Method to log in user"""
        # Creating user in database
        user = User.objects.create(
            username=TEST_USERNAME, 
            email=TEST_EMAIL,
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            phone_number=TEST_PHONE_NUMBER,
            mode='seller',
            description=TEST_DESCRIPTION,
        )
        user.set_password(TEST_PASSWORD)
        user.save()
        address = Address.objects.create(
            first_line=TEST_ADDRESS_FIRST_LINE,
            second_line=TEST_ADDRESS_SECOND_LINE,
            city=TEST_CITY,
            postcode=TEST_POSTCODE,
            user=user
        )
        address.save()

        # Retrieve url
        self.get_url('login')

        # Fill in fields
        self.selenium.find_element(By.NAME, 'user').send_keys(TEST_USERNAME)
        self.selenium.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)

        # Submit form
        self.selenium.find_element(By.ID, 'submit').click()

    # def test_signup(self):
    #     # Retrieve url
    #     self.get_url('signup')

    #     # Fill in fields
    #     self.selenium.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
    #     self.selenium.find_element(By.NAME, 'first_name').send_keys(TEST_FIRST_NAME)
    #     self.selenium.find_element(By.NAME, 'last_name').send_keys(TEST_LAST_NAME)
    #     self.selenium.find_element(By.NAME, 'phone_number').send_keys(TEST_PHONE_NUMBER)
    #     self.selenium.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
    #     self.selenium.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
    #     self.selenium.find_element(By.NAME, 'reenter_password').send_keys(TEST_PASSWORD)
    #     self.selenium.find_element(By.NAME, 'last_name').send_keys(TEST_LAST_NAME)
    #     self.selenium.find_element(By.NAME, 'theme_preference').click()
    #     self.selenium.find_element(By.XPATH, "//option[@value='dark']").click()
    #     self.selenium.find_element(By.NAME, 'mode').click()
    #     self.selenium.find_element(By.XPATH, "//option[@value='seller']").click()
    #     self.selenium.find_element(By.NAME, 'description').send_keys(TEST_DESCRIPTION)
    #     self.selenium.find_element(By.NAME, 'first_line').send_keys(TEST_ADDRESS_FIRST_LINE)
    #     self.selenium.find_element(By.NAME, 'second_line').send_keys(TEST_ADDRESS_SECOND_LINE)
    #     self.selenium.find_element(By.NAME, 'city').send_keys(TEST_CITY)
    #     self.selenium.find_element(By.NAME, 'postcode').send_keys(TEST_POSTCODE)

    #     # Submit form
    #     self.selenium.find_element(By.ID, 'submit').click()

    #     time.sleep(2) # Accounting for processing delay

    #     # Ensuring url has updated to details page
    #     self.assertEqual(self.selenium.current_url, 'http://localhost:5173/details')
    
    # def test_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     # Retrieve url
    #     self.get_url('login')

    #     # Fill in fields
    #     self.selenium.find_element(By.NAME, 'user').send_keys(TEST_USERNAME)
    #     self.selenium.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)

    #     # Submit form
    #     self.selenium.find_element(By.ID, 'submit').click()

    #     time.sleep(2) # Accounting for processing delay

    #     # Ensuring url has updated to home page
    #     self.assertEqual(self.selenium.current_url, 'http://localhost:5173/')
    
    # def test_back_signup(self):
    #     self.get_url('signup') # Retrieve url
    #     self.selenium.find_element(By.ID, 'home').click() # Click home
    #     self.assertEqual(self.selenium.current_url, 'http://localhost:5173/') # Ensuring url has updated to home page
    
    # def test_back_login(self):
    #     self.get_url('login')
    #     self.selenium.find_element(By.ID, 'home').click() 
    #     self.assertEqual(self.selenium.current_url, 'http://localhost:5173/')
    
    def test_settings(self):
        self.buyer_login()
        self.get_url('settings')
        user: User = User.objects.first()
        self.assertEqual(user.theme_preference, 'light') 
        self.selenium.find_element(By.ID, 'toggle').click() 
        # self.assertEqual(user.theme_preference, 'dark') 
        time.sleep(8)

    # def test_buyer_menu_navigation(self):
    #     self.buyer_login()
    #     time.sleep(5) # Processing time

    #     # Home page
    #     # self.selenium.find_element(By.ID, 'logo').click() 
    #     # self.assertEqual(self.selenium.current_url, 'http://localhost:5173/') 
    #     # self.selenium.find_element(By.LINK_TEXT, 'Home').click() 
    #     # self.assertEqual(self.selenium.current_url, 'http://localhost:5173/')
    #     WebDriverWait(self.selenium, 10).until(
    #         expected_conditions.element_to_be_clickable((By.LINK_TEXT, 'Settings'))
    #     )
    #     self.selenium.find_element(By.LINK_TEXT, 'Settings').click() 
    #     time.sleep(50)
    #     self.assertEqual(self.selenium.current_url, 'http://localhost:5173/settings') 
