import json
from django.core.management import call_command
from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser
from api.models import Address, CartResource, Exchange, Message, Messages, Order, OrderResource, Resource, Review, Subject, User

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
        call_command('update_rates')
        user = User.objects.create(
            username='admin', 
            email='admin@gmail.com',
            first_name='ad',
            last_name='min',
            phone_number='072332232',
            mode='buyer',
            theme_preference=TEST_THEME,
        )
        user.set_password(TEST_PASSWORD)
        user.save()
        user2 = User.objects.create(
            username='admin0', 
            email='admin0@gmail.com',
            first_name='admin',
            last_name='one',
            phone_number='072332299',
            mode='buyer',
            theme_preference=TEST_THEME,
        )
        user2.set_password(TEST_PASSWORD)
        user2.save()
        Subject.objects.create(name='Biology', user=user)
        Subject.objects.create(name='Media Studies', user=user)
        Subject.objects.create(name='Computer Science', user=user)
        Subject.objects.create(name='Chemistry', user=user)
        Subject.objects.create(name='Physics', user=user)
        address = Address.objects.create(
            first_line=TEST_ADDRESS_FIRST_LINE,
            second_line=TEST_ADDRESS_SECOND_LINE,
            city=TEST_CITY,
            postcode=TEST_POSTCODE,
            user=user
        )
        address.save()
        resource = Resource.objects.create(
            name='Test Resource',
            description='A test description for the resource.',
            height=20.5,
            width=15.2,
            weight=1.2,
            price=1.00,
            stock=50,
            estimated_delivery_time=5,
            subject='Mathematics',
            author='John Doe',
            self_made=True,
            is_draft=False,
            unique=True,
            allow_delivery=False,
            allow_collection=False,
            allow_return=False,
            page_start=1,
            page_end=100,
            height_unit='cm',
            width_unit='cm',
            image1='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            image2='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            video='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            upload_date=timezone.now(),
            last_edited=timezone.now(),
            user=user,  
            weight_unit='kg',
            price_currency='GBP',
            estimated_delivery_units='days',
            type='Textbook', 
            colour='Blue',
            source='AI',
            condition='New',
            media='Online',
        )
        resource.save()
        resource1 = Resource.objects.create(
            name='Test Resource',
            description='A test description for the resource.',
            height=20.5,
            width=15.2,
            weight=1.2,
            price=1.00,
            stock=50,
            estimated_delivery_time=5,
            subject='Mathematics',
            author='John Doe',
            self_made=True,
            is_draft=False,
            unique=True,
            allow_delivery=False,
            allow_collection=False,
            allow_return=False,
            page_start=1,
            page_end=100,
            height_unit='cm',
            width_unit='cm',
            image1='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            image2='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            video='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            upload_date=timezone.now(),
            last_edited=timezone.now(),
            user=user2,  
            weight_unit='kg',
            price_currency='GBP',
            estimated_delivery_units='days',
            type='Textbook', 
            colour='Blue',
            source='AI',
            condition='New',
            media='Online',
        )
        resource1.save()
        resource2 = Resource.objects.create(
            name='Mathematics Revision Guide',
            description='A test description for the resource.',
            height=20.5,
            width=15.2,
            weight=1.2,
            price=1.00,
            stock=50,
            estimated_delivery_time=5,
            subject='Chemistry',
            author='John Doe',
            self_made=True,
            is_draft=False,
            unique=True,
            allow_delivery=False,
            allow_collection=False,
            allow_return=False,
            page_start=1,
            page_end=100,
            height_unit='cm',
            width_unit='cm',
            image1='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            image2='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            video='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            upload_date=timezone.now(),
            last_edited=timezone.now(),
            user=user,  
            weight_unit='kg',
            price_currency='GBP',
            estimated_delivery_units='days',
            type='Textbook', 
            colour='Blue',
            source='AI',
            condition='New',
            media='Online',
        )
        resource2.save()
        resource3 = Resource.objects.create(
            name='English Book',
            description='A test description for the resource.',
            height=20.5,
            width=15.2,
            weight=1.2,
            price=1.00,
            stock=50,
            estimated_delivery_time=5,
            subject='English',
            author='John Doe',
            self_made=True,
            is_draft=False,
            unique=True,
            allow_delivery=False,
            allow_collection=False,
            allow_return=False,
            page_start=1,
            page_end=100,
            height_unit='cm',
            width_unit='cm',
            image1='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            image2='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            video='https://m.media-amazon.com/images/I/51+yjR0P2ML._SY445_SX342_.jpg', 
            upload_date=timezone.now(),
            last_edited=timezone.now(),
            user=user,  
            weight_unit='kg',
            price_currency='GBP',
            estimated_delivery_units='days',
            type='Textbook', 
            colour='Blue',
            source='AI',
            condition='New',
            media='Online',
        )
        resource3.save()
    
    # def test_valid_signup(self):
    #     # Beginning of code taken from ECS639U socialnetwork_v2 folder
    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': TEST_FIRST_NAME,
    #         'last_name': TEST_LAST_NAME,
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD,
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)
    #     self.assertEqual(response.request['PATH_INFO'], '/details')
    
    # def test_invalid_format_signup(self):
    #     """Testing when input is in invalid format"""
    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': 'a',
    #         'first_name': '@',
    #         'last_name': '@',
    #         'phone_number': ']',
    #         'username': '#',
    #         'password': 'o',
    #         'reenter_password': 'l',
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': 'two  spaces',
    #         'first_line': 'two  spaces',
    #         'second_line': 'two  spaces',
    #         'city': 'two  spaces',
    #         'postcode': 'toomanycharacters',
    #     }, follow=True)
    #     self.assertContains(response, 'Enter a valid email address')
    #     self.assertEqual(response.content.decode().count('Only letters are allowed'), 2)
    #     self.assertContains(response, 'Username cannot contain special characters')
    #     self.assertContains(response, 'Must be 10 or 11 digit number starting with 07')
    #     self.assertContains(response, 'Username cannot contain special characters')
    #     self.assertContains(response, 'Password must be between 8 to 15 characters long')
    #     self.assertEqual(response.content.decode().count('Only one space between words'), 4)
    #     self.assertContains(response, 'Ensure this value has at most 7 characters')
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/') # Ensure no page redirect

    #     # Trying where first name and last name have two spaces between words
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': 'invalid  input',
    #         'last_name': 'invalid  input',
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD,
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)
    #     self.assertEqual(response.content.decode().count('Only one space between words'), 2)
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    # def test_empty_inputs_signup(self):
    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': '',
    #         'first_name': '',
    #         'last_name': '',
    #         'phone_number': '',
    #         'username': '',
    #         'password': '',
    #         'reenter_password': '',
    #         'theme_preference': 'light', # Default value
    #         'mode': 'seller', # Seller added to ensure description field is visible
    #         'description': '',
    #         'first_line': '',
    #         'second_line': '',
    #         'city': '',
    #         'postcode': '',
    #     }, follow=True)

    #     self.assertEqual(response.content.decode().count('This field is required'), 11)
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')

    # def test_existing_username_signup(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': TEST_FIRST_NAME,
    #         'last_name': TEST_LAST_NAME,
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD,
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)

    #     self.assertContains(response, 'A user with that username already exists')
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')

    # def test_existing_email_signup(self):
    #     # Creating user in database
    #     user = User.objects.create(username='test123')
    #     user.set_password(TEST_PASSWORD)
    #     user.email = TEST_EMAIL
    #     user.save()

    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': TEST_FIRST_NAME,
    #         'last_name': TEST_LAST_NAME,
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD,
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)

    #     self.assertContains(response, 'User with this Email already exists')
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    # def test_existing_number_signup(self):
    #     # Creating user in database
    #     user = User.objects.create(username='test123')
    #     user.set_password(TEST_PASSWORD)
    #     user.phone_number = TEST_PHONE_NUMBER
    #     user.save()

    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': TEST_FIRST_NAME,
    #         'last_name': TEST_LAST_NAME,
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD,
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)

    #     self.assertContains(response, 'User with this Phone number already exists')
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    # def test_mismatched_password_signup(self):
    #     url = reverse('api:signup') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'email': TEST_EMAIL,
    #         'first_name': TEST_FIRST_NAME,
    #         'last_name': TEST_LAST_NAME,
    #         'phone_number': TEST_PHONE_NUMBER,
    #         'username': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #         'reenter_password': TEST_PASSWORD+'1',
    #         'theme_preference': TEST_THEME,
    #         'mode': TEST_MODE,
    #         'description': TEST_DESCRIPTION,
    #         'first_line': TEST_ADDRESS_FIRST_LINE,
    #         'second_line': TEST_ADDRESS_SECOND_LINE,
    #         'city': TEST_CITY,
    #         'postcode': TEST_POSTCODE,
    #     }, follow=True)

    #     self.assertContains(response, 'Both passwords must match')
    #     self.assertEqual(response.request['PATH_INFO'], '/signup/')
    
    # def test_valid_email_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': TEST_EMAIL,
    #         'password': TEST_PASSWORD,
    #     }, follow=True)

    #     self.assertEqual(response.request['PATH_INFO'], '/')
    
    # def test_valid_username_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': TEST_USERNAME,
    #         'password': TEST_PASSWORD,
    #     }, follow=True)

    #     self.assertEqual(response.request['PATH_INFO'], '/')
    
    # def test_valid_buyer_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL, mode='buyer')
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': TEST_EMAIL,
    #         'password': TEST_PASSWORD,
    #     }, follow=True)

    #     self.assertEqual(response.request['PATH_INFO'], '/')
    
    # def test_valid_seller_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL, mode='seller')
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': TEST_EMAIL,
    #         'password': TEST_PASSWORD,
    #     }, follow=True)
    #     self.assertEqual(response.request['PATH_INFO'], '/listings')
    
    # def test_empty_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': '',
    #         'password': '',
    #     }, follow=True)

    #     self.assertEqual(response.content.decode().count('This field is required'), 2)
    #     self.assertEqual(response.request['PATH_INFO'], '/login/')
    
    # def test_incorrect_password_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': TEST_EMAIL,
    #         'password': 'wrongpass123',
    #     }, follow=True)
        
    #     self.assertEqual(response.request['PATH_INFO'], '/login/')
    #     self.assertContains(response, 'Invalid email or password')

    # def test_incorrect_username_login(self):
    #     # Creating user in database
    #     user = User.objects.create(username=TEST_USERNAME, email=TEST_EMAIL)
    #     user.set_password(TEST_PASSWORD)
    #     user.save()

    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': 'wrongusername',
    #         'password': TEST_PASSWORD,
    #     }, follow=True)
        
    #     self.assertEqual(response.request['PATH_INFO'], '/login/')
    #     self.assertContains(response, 'Invalid username or password')
    
    # def test_incorrect_login(self):
    #     url = reverse('api:login') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertContains(response, 'csrfmiddlewaretoken') # Check inclusion of csrfmiddlewaretoken
    #     soup = BeautifulSoup(response.content, features="html.parser")
    #     csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    #     response = self.client.post(url, {
    #         'csrfmiddlewaretoken': csrf_token['value'],
    #         'user': 'wrongusername',
    #         'password': 'wrongpass',
    #     }, follow=True)
        
    #     self.assertEqual(response.request['PATH_INFO'], '/login/')
    #     self.assertContains(response, 'Invalid username or password')

    # def buyer_user(self):
    #     user = User.objects.create(
    #         username=TEST_USERNAME, 
    #         email=TEST_EMAIL,
    #         first_name=TEST_FIRST_NAME,
    #         last_name=TEST_LAST_NAME,
    #         phone_number=TEST_PHONE_NUMBER,
    #         mode='buyer',
    #         theme_preference=TEST_THEME,
    #     )
    #     user.set_password(TEST_PASSWORD)
    #     user.save()
    #     address = Address.objects.create(
    #         first_line=TEST_ADDRESS_FIRST_LINE,
    #         second_line=TEST_ADDRESS_SECOND_LINE,
    #         city=TEST_CITY,
    #         postcode=TEST_POSTCODE,
    #         user=user
    #     )
    #     address.save()

    # def seller_user(self):
    #     user = User.objects.create(
    #         username=TEST_USERNAME, 
    #         email=TEST_EMAIL,
    #         first_name=TEST_FIRST_NAME,
    #         last_name=TEST_LAST_NAME,
    #         phone_number=TEST_PHONE_NUMBER,
    #         mode='seller',
    #         description=TEST_DESCRIPTION,
    #         theme_preference=TEST_THEME,
    #     )
    #     user.set_password(TEST_PASSWORD)
    #     user.save()
    #     address = Address.objects.create(
    #         first_line=TEST_ADDRESS_FIRST_LINE,
    #         second_line=TEST_ADDRESS_SECOND_LINE,
    #         city=TEST_CITY,
    #         postcode=TEST_POSTCODE,
    #         user=user
    #     )
    #     address.save()

    # def test_signout(self):
    #     self.client.login(username='admin', password=TEST_PASSWORD)
    #     url = reverse('health') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     # Ensure currently signed in user is admin
    #     self.assertEqual(response.wsgi_request.user.username, 'admin')
    #     self.assertEqual(response.status_code, 200)
    #     url = reverse('api:signout') # Retrieve path
    #     response = self.client.get(url) # Retrieve response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    # def test_user(self):
    #     # Checking that unauthenticated is returned
    #     url = reverse('api:user') 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['user'], 'unauthenticated')
    #     # Checking that a dict with 24 keys is returned
    #     self.client.login(username='admin', password=TEST_PASSWORD)
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(json.loads(response.content)['user']), 24)
    
    # def test_users(self):
    #     self.buyer_user()
    #     url = reverse('api:users') 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     # Checking there are three users, each with 24 items
    #     self.assertEqual(len(json.loads(response.content)), 3)
    #     self.assertEqual(len(json.loads(response.content)[0]), 24)
    
    # def test_delete_account(self):
    #     self.buyer_user()
    #     url = reverse('api:review') 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(json.loads(response.content)), 2)
    #     self.assertEqual(len(json.loads(response.content)[0]), 37)

    # def test_delete_account(self):
    #     self.buyer_user()
    #     url = reverse('api:delete account', kwargs={
    #         'user' : 1
    #     }) 
    #     response = self.client.delete(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.filter(id=1).exists(), False)

    # def test_update_details(self):
    #     self.buyer_user()
        
    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'theme'}) 
    #     response = self.client.put(url, data=json.dumps('light'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).theme_preference, 'light')
        
    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'currency'}) 
    #     response = self.client.put(url, data=json.dumps('EUR'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).currency, 'EUR')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'mode'}) 
    #     response = self.client.put(url, data=json.dumps('seller'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).mode, 'seller')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'email'}) 
    #     response = self.client.put(url, data=json.dumps('newemail@gmail.com'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).email, 'newemail@gmail.com')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'username'}) 
    #     response = self.client.put(url, data=json.dumps('admin1'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).username, 'admin1')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'password'}) 
    #     response = self.client.put(url, data=json.dumps('password123'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).check_password('password123'), True)

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'name'}) 
    #     response = self.client.put(url, data=json.dumps('newname'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).first_name, 'newname')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'surname'}) 
    #     response = self.client.put(url, data=json.dumps('surname'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).last_name, 'surname')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'number'}) 
    #     response = self.client.put(url, data=json.dumps('0712345683'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).phone_number, '0712345683')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'description'}) 
    #     response = self.client.put(url, data=json.dumps('A new updated description.'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).description, 'A new updated description.')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'address_line_one'}) 
    #     response = self.client.put(url, data=json.dumps('new line one'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Address.objects.get(user__id=1).first_line, 'new line one')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'address_line_two'}) 
    #     response = self.client.put(url, data=json.dumps('new line two'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Address.objects.get(user__id=1).second_line, 'new line two')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'city'}) 
    #     response = self.client.put(url, data=json.dumps('new city'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Address.objects.get(user__id=1).city, 'new city')

    #     url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'postcode'}) 
    #     response = self.client.put(url, data=json.dumps('new post'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Address.objects.get(user__id=1).postcode, 'new post')

    #     url = reverse('api:details', kwargs={'id' : 1, 'attribute' : 'subjects'}) 
    #     response = self.client.put(url, data=json.dumps('English'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Subject.objects.filter(user__id=1, name='English').exists())
    #     # Delete subject
    #     response = self.client.delete(url, data=json.dumps(Subject.objects.get(name='English').id), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Subject.objects.filter(user__id=1, name='English').exists())

    # def test_check_details_email(self):
    #     self.buyer_user()
    #     url = reverse('api:check details', kwargs={
    #         'id' : 1,
    #         'attribute' : 'email'
    #     }) 
    #     response = self.client.put(url,
    #         data=json.dumps(TEST_EMAIL),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), True)
    #     response = self.client.put(url,
    #         data=json.dumps('nonexistentemail@gmail.com'),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), False)
    
    # def test_check_details_username(self):
    #     self.buyer_user()
    #     url = reverse('api:check details', kwargs={
    #         'id' : 1,
    #         'attribute' : 'username'
    #     }) 
    #     response = self.client.put(url,
    #         data=json.dumps(TEST_USERNAME),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), True)
    #     response = self.client.put(url,
    #         data=json.dumps('nonexistentusername'),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), False)
    
    # def test_check_details_number(self):
    #     self.buyer_user()
    #     url = reverse('api:check details', kwargs={
    #         'id' : 1,
    #         'attribute' : 'number'
    #     }) 
    #     response = self.client.put(url,
    #         data=json.dumps(TEST_PHONE_NUMBER),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), True)
    #     response = self.client.put(url,
    #         data=json.dumps('0711111118'),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), False)
    
    # def test_check_details_password(self):
    #     self.buyer_user()
    #     url = reverse('api:check details', kwargs={
    #         'id' : 1,
    #         'attribute' : 'password'
    #     }) 
    #     response = self.client.put(url,
    #         data=json.dumps(TEST_PASSWORD),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), True)
    #     response = self.client.put(url,
    #         data=json.dumps('nfdsd'),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content), False)
    
    # def test_semantic_subjects(self):
    #     self.buyer_user()
    #     url = reverse('api:semantic search subjects') 
    #     response = self.client.post(url,
    #         data=json.dumps('atom'),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)[0], 'Chemistry')

    # def test_resources(self):
    #     self.buyer_user()
    #     url = reverse('api:resources') 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     # Checking there are four users, each with 24 items
    #     self.assertEqual(len(json.loads(response.content)), 4)
    #     self.assertEqual(len(json.loads(response.content)[0]), 37)

    # def test_handle_listing(self):
    #     self.buyer_user()
    #     url = reverse('api:new listing', kwargs={
    #         'id' : 1,
    #     }) 
    #     response = self.client.post(url,
    #         data={
    #             'name': 'Test Resource 3',
    #             'description': 'A test description for the resource.',
    #             'height': 20.5,
    #             'width': 15.2,
    #             'weight': 1.2,
    #             'price': 1.00,
    #             'stock': 50,
    #             'estimated_number': 5,
    #             'subject': 'Chemistry',
    #             'author': 'John Doe',
    #             'self_made': True,
    #             'is_draft': False,
    #             'unique': True,
    #             'allow_delivery': False,
    #             'allow_collection': False,
    #             'allow_return': False,
    #             'page_start': 1,
    #             'page_end': 100,
    #             'height_unit': 'cm',
    #             'width_unit': 'cm',
    #             'image1': SimpleUploadedFile('test.jpg', b''), 
    #             'image2': SimpleUploadedFile('test.jpg', b''), 
    #             'video': SimpleUploadedFile('test.mp4', b''), 
    #             'weight_unit': 'kg',
    #             'price_currency': 'GBP',
    #             'estimated_units': 'days',
    #             'type': 'Textbook', 
    #             'colour': 'Blue',
    #             'source': 'AI',
    #             'condition': 'New',
    #             'media': 'Online',
    #         },
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     id = json.loads(response.content)['id']
    #     # Check if created ID exists in database
    #     self.assertTrue(Resource.objects.filter(id=id).exists())

    #     # Edit old listing
    #     response = self.client.post(url,
    #         data={
    #             'id': json.loads(response.content)['id'],
    #             'name': 'Test Resource 3 - Edited',
    #             'description': 'An edited test description for the resource.',
    #             'height': 20.51,
    #             'width': 15.21,
    #             'weight': 1.21,
    #             'price': 1.001,
    #             'stock': 501,
    #             'estimated_number': 6,
    #             'subject': 'Maths',
    #             'author': 'John Doent',
    #             'self_made': False,
    #             'is_draft': True,
    #             'unique': False,
    #             'allow_delivery': True,
    #             'allow_collection': True,
    #             'allow_return': True,
    #             'page_start': 1,
    #             'page_end': 2,
    #             'height_unit': 'm',
    #             'width_unit': 'm',
    #             'image1': SimpleUploadedFile('test0.jpg', b''), 
    #             'image2': SimpleUploadedFile('test0.jpg', b''), 
    #             'video': SimpleUploadedFile('test0.mp4', b''), 
    #             'weight_unit': 'g',
    #             'price_currency': 'EUR',
    #             'estimated_units': 'months',
    #             'type': 'Note', 
    #             'colour': 'Red',
    #             'source': 'Internet',
    #             'condition': 'Used',
    #             'media': 'Paper',
    #         },
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     # Checking name has updated
    #     self.assertTrue(Resource.objects.get(id=id).name == 'Test Resource 3 - Edited')

    #     # Delete resource
    #     response = self.client.delete(url,
    #         data=json.dumps(id),
    #         content_type='application/json'
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Resource.objects.filter(id=id).exists())

    # def test_reviews(self):
    #     self.buyer_user()
    #     # Create review
    #     url = reverse('api:review', kwargs={
    #         'user' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url,
    #         data={
    #             'title': 'Great product',
    #             'stars': 4,
    #             'description': 'No issues, nice product.',
    #             'image': SimpleUploadedFile('test.jpg', b''), 
    #             'video': SimpleUploadedFile('test.mp4', b''), 
    #         }
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Review.objects.count(), 1)
    #     self.assertEqual(Resource.objects.get(id=1).rating, 4)

    #     # Edit review
    #     url = reverse('api:edit review', kwargs={
    #         'user' : 1,
    #         'id' : Review.objects.first().id,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url,
    #         data={
    #             'old_resource': Review.objects.first().id,
    #             'title': 'Great product - Edited',
    #             'stars': 2,
    #             'description': 'No issues yet, nice product.',
    #             'image': SimpleUploadedFile('test0.jpg', b''), 
    #             'video': SimpleUploadedFile('test0.mp4', b''), 
    #         }
    #     ) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Review.objects.first().title, 'Great product - Edited')
    #     self.assertEqual(Resource.objects.get(id=1).rating, 2)

    #     # Delete review
    #     url = reverse('api:review', kwargs={
    #         'user' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.delete(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Review.objects.count(), 0)
    #     self.assertEqual(Resource.objects.get(id=1).rating, 0)
    
    # def test_sentiment_analysis(self):
    #     Review.objects.create(
    #         title='Great product',
    #         rating=4,
    #         review='Great product',
    #         resource=Resource.objects.get(id=1),
    #         user=User.objects.get(id=1)
    #     )
    #     Review.objects.create(
    #         title='Bad product',
    #         rating=1,
    #         review='Bad product.',
    #         resource=Resource.objects.get(id=1),
    #         user=User.objects.get(id=1)
    #     )

    #     url = reverse('api:sentiment analysis', kwargs={
    #         'resource' : 'Test Resource'
    #     }) 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(next(iter(sorted(json.loads(response.content).items(), key=lambda x: x[1], reverse=True)))[0], '1')

    # def test_cart(self):
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     # Add cart item
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 1)

    #     # Update cart
    #     response = self.client.put(url, data=json.dumps(5), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(CartResource.objects.get(id=1).number, 5)

    #     # Get cart
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['items'], 5)
    #     url = reverse('api:get cart', kwargs={
    #         'user' : 1,
    #     }) 
    #     response = self.client.get(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['items'], 5)

    #     # Delete cart item
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.delete(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 0)

    # def test_wishlist(self):
    #     url = reverse('api:update wishlist', kwargs={'user' : 1}) 
    #     # Add wishlist item
    #     response = self.client.post(url, data=json.dumps(1), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).wishlist.items, 1)

    #     # Wishlist to cart
    #     response = self.client.put(url, data=json.dumps(1), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).wishlist.items, 0)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 1)

    #     # Cart to wishlist
    #     url = reverse('api:cart to wishlist', kwargs={'user' : 1}) 
    #     response = self.client.put(url, data=json.dumps(1), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).wishlist.items, 1)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 0)

    #     # Delete wishlist item
    #     url = reverse('api:update wishlist', kwargs={'user' : 1}) 
    #     response = self.client.delete(url, data=json.dumps(1), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).wishlist.items, 0)
    
    # def test_order(self):
    #     # Add cart item
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 1)
        
    #     # Place order, checking cart has been cleared and order instance is made
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 0)
    #     self.assertTrue(Order.objects.filter(id=1, buyer__id=1, seller__id=1).exists())
       
    #     # Update order status
    #     response = self.client.put(url, data=json.dumps({'id': 1, 'status': 'Processing'}), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Order.objects.get(id=1, buyer__id=1, seller__id=1).status, 'Processing')

    #     # Delete order
    #     response = self.client.delete(url, data=json.dumps(1), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Order.objects.get(id=1, buyer__id=1, seller__id=1).status, 'Cancelled')

    #     # Add cart item
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 1)
    #     # 'Buy Now' order
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.post(url, data=json.dumps(2), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.get(id=1).cart.items, 0)
    #     self.assertTrue(Order.objects.filter(id=2, buyer__id=1, seller__id=1, status='Placed').exists())
    
    # def test_semantic_orders(self):
    #     self.buyer_user()
    #     # Add cart items
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 3
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 4
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
        
    #     # Place order, checking cart has been cleared and order instance is made
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
       
    #     url = reverse('api:semantic search orders', kwargs={
    #         'id' : 1,
    #         'search' : 'mathematics guide',
    #         'mode': 'buyer'
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)[0], 1)

    # def test_exchange(self):
    #     # Create exchange
    #     url = reverse('api:exchange', kwargs={
    #         'user' : 1,
    #         'seller' : 2,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Exchange.objects.filter(id=1, user1__id=1, user2__id=2).exists())
        
    #     # Update status
    #     response = self.client.put(url, data=json.dumps({'field' : 'resource', 'data' : 3})) 
    #     response = self.client.put(url, data=json.dumps({'field' : 'user1', 'data' : 3})) 
    #     response = self.client.put(url, data=json.dumps({'field' : 'user2', 'data' : 3})) 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Exchange.objects.filter(id=1, user1__id=1, user2__id=2, resource1=3, resource1_number=3, resource2_number=3).exists())

    #     # Get instance
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(json.loads(response.content)), 9)

    #     # Place order
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.post(url, data=json.dumps({'exchange_id': 1}), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Order.objects.filter(id=1, buyer__id=2, seller__id=1).exists())

    #     # Delete instance
    #     url = reverse('api:exchange', kwargs={
    #         'user' : 1,
    #         'seller' : 2,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     url = reverse('api:exchange', kwargs={
    #         'user' : 1,
    #         'seller' : 2,
    #         'resource' : 2
    #     }) 
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(Exchange.objects.filter(id=1, user1__id=1, user2__id=2).exists())

    # def test_return(self):
    #     # Place order
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     # Add items for return
    #     url = reverse('api:toggle return', kwargs={
    #         'user' : 1,
    #         'order' : 1,
    #         'resource' : 1,
    #     }) 
    #     response = self.client.put(url, data=json.dumps(1), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(OrderResource.objects.get(id=1).number_for_return, 1)

    #     # Submit return
    #     url = reverse('api:submit_return', kwargs={
    #         'user' : 1,
    #         'order' : 1,
    #     }) 
    #     response = self.client.put(url, data=json.dumps({'cancel': 'false', 'return_method': 'Collection', 'return_reason': ''}), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Order.objects.filter(id=1, status='Return Started').exists())
    
    # def test_semantic_search(self):
    #     url = reverse('api:semantic search', kwargs={
    #         'user' : 1,
    #     }) 
    #     response = self.client.post(url, data=json.dumps('numbers'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)[0]['name'], 'Mathematics Revision Guide')

    # def test_messages(self):
    #     # Create message between two users
    #     url = reverse('api:messages', kwargs={
    #         'user1' : 1,
    #         'user2' : 2,
    #     }) 
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, 200)
    #     last_seen = Messages.objects.get(id=1).user1_seen

    #     url = reverse('api:message', kwargs={
    #         'id' : 1,
    #         'sender' : 1,
    #     }) 
    #     # Ensuring last seen is updated
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotEqual(last_seen, Messages.objects.get(id=1).user1_seen)

    #     # Sending message
    #     response = self.client.post(url, data=json.dumps('First message'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Message.objects.get(id=1).message, 'First message')

    # def test_feedback(self):
    #     url = reverse('api:feedback')
    #     response = self.client.post(url, data=json.dumps('Great app'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     email = mail.outbox[0]
    #     self.assertEqual(email.subject, 'Feedback submitted')
    #     self.assertEqual(email.body, 'Great app')
    #     self.assertEqual(email.from_email, 'edusource9325@gmail.com')
    #     self.assertIn('edusource9325@gmail.com', email.to)

    # def test_recommendations(self):
    #     url = reverse('api:recommendations', kwargs={
    #         'user' : 1,
    #     }) 
    #     # Ensuring last seen is updated
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotIn('English', json.loads(response.content)[0].values())
    #     self.assertIn('Chemistry', json.loads(response.content)[0].values())

    # def test_chatbot(self):
    #     url = reverse('api:chatbot', kwargs={
    #         'user' : -1,
    #     }) 
    #     response = self.client.post(url, data=json.dumps('What is the status of order 1'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('You must be signed in to verify this', json.loads(response.content))
    #     response = self.client.post(url, data=json.dumps('Provide me with personalised recommendations'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('You must be signed in for this to be available', json.loads(response.content))

    #     url = reverse('api:chatbot', kwargs={
    #         'user' : 1,
    #     }) 
    #     response = self.client.post(url, data=json.dumps('What is the status of order'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Sorry, I do not recogise that order number', json.loads(response.content))

    #     # Place order
    #     url = reverse('api:update cart', kwargs={
    #         'user' : 1,
    #         'cart' : 1,
    #         'resource' : 1
    #     }) 
    #     response = self.client.post(url) 
    #     self.assertEqual(response.status_code, 200)
    #     url = reverse('api:order', kwargs={'user': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    #     url = reverse('api:chatbot', kwargs={
    #         'user' : 1,
    #     }) 
    #     response = self.client.post(url, data=json.dumps('What is the status of order 1'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Placed', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Provide me with personalised recommendations'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Below are some recommendations', json.loads(response.content))

    #     url = reverse('api:chatbot', kwargs={
    #         'user' : 2,
    #     }) 
    #     response = self.client.post(url, data=json.dumps('Provide me with personalised recommendations'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Sorry, I cannot do that as you do not have any personalised recommendations yet', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Can you provide resource recommendations for'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Please repeat the statement with a recommendation', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Can you provide resource recommendations for chemistry'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Below are some recommendations', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Can you provide resource recommendations for cat'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Sorry. We were unable to find resources matching your query', json.loads(response.content))

    #     # Known questions and answers
    #     response = self.client.post(url, data=json.dumps('How do I place an order'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('There are two ways to do this', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I exchange resources?'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select a resource you want to exchange', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I list items'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select the +', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I track an order'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('View Order Status', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I start a return'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select Return Method', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Do you provide resource recommendations'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Of course', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('Where is my wishlist'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select Wishlist', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How can I find my wishlist'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select Wishlist', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How can I find my order details'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Log in and click', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I compare resources'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('You can compare a maximum of', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How do I delete my account'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('at the bottom of the page', json.loads(response.content))

    #     response = self.client.post(url, data=json.dumps('How can I view messages'), content_type='application/json') 
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Select Messages', json.loads(response.content))

    def test_gbp_usd(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'USD',
            'to_currency' : 'GBP',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('1.33', json.loads(response.content)['new_price'])

    def test_usd_gbp(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'GBP',
            'to_currency' : 'USD',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('0.75', json.loads(response.content)['new_price'])

    def test_gbp_eur(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'EUR',
            'to_currency' : 'GBP',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('1.17', json.loads(response.content)['new_price'])
    
    def test_eur_gbp(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'GBP',
            'to_currency' : 'EUR',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('0.85', json.loads(response.content)['new_price'])
    
    def test_eur_usd(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'USD',
            'to_currency' : 'EUR',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('1.14', json.loads(response.content)['new_price'])
    
    def test_eur_gbp(self):
        url = reverse('api:currency conversion', kwargs={
            'id' : 1,
            'from_currency' : 'EUR',
            'to_currency' : 'USD',
        }) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('0.88', json.loads(response.content)['new_price'])