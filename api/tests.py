from decimal import Decimal
import json
from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from api.models import Address, Resource, Subject, User

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
        address = Address.objects.create(
            first_line=TEST_ADDRESS_FIRST_LINE,
            second_line=TEST_ADDRESS_SECOND_LINE,
            city=TEST_CITY,
            postcode=TEST_POSTCODE,
            user=user
        )
        address.save()
        resource1 = Resource.objects.create(
            name='Test Resource',
            description='A test description for the resource.',
            height=Decimal('20.5'),
            width=Decimal('15.2'),
            weight=Decimal('1.2'),
            price=Decimal('1.00'),
            stock=Decimal('50'),
            estimated_delivery_time=Decimal('5'),
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
            rating=Decimal('4.5'),
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
        resource1.save()
        resource2 = Resource.objects.create(
            name='Test Resource Two',
            description='A test description for the resource.',
            height=Decimal('20.5'),
            width=Decimal('15.2'),
            weight=Decimal('1.2'),
            price=Decimal('1.00'),
            stock=Decimal('50'),
            estimated_delivery_time=Decimal('5'),
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
            rating=Decimal('4.5'),
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

    def buyer_user(self):
        user = User.objects.create(
            username=TEST_USERNAME, 
            email=TEST_EMAIL,
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            phone_number=TEST_PHONE_NUMBER,
            mode='buyer',
            theme_preference=TEST_THEME,
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

    def seller_user(self):
        user = User.objects.create(
            username=TEST_USERNAME, 
            email=TEST_EMAIL,
            first_name=TEST_FIRST_NAME,
            last_name=TEST_LAST_NAME,
            phone_number=TEST_PHONE_NUMBER,
            mode='seller',
            description=TEST_DESCRIPTION,
            theme_preference=TEST_THEME,
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

    def test_signout(self):
        self.client.login(username='admin', password=TEST_PASSWORD)
        url = reverse('health') # Retrieve path
        response = self.client.get(url) # Retrieve response
        # Ensure currently signed in user is admin
        self.assertEqual(response.wsgi_request.user.username, 'admin')
        self.assertEqual(response.status_code, 200)
        url = reverse('api:signout') # Retrieve path
        response = self.client.get(url) # Retrieve response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_user(self):
        # Checking that unauthenticated is returned
        url = reverse('api:user') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['user'], 'unauthenticated')
        # Checking that a dict with 24 keys is returned
        self.client.login(username='admin', password=TEST_PASSWORD)
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['user']), 24)
    
    def test_users(self):
        self.buyer_user()
        url = reverse('api:users') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        # Checking there are two users, each with 24 items
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(len(json.loads(response.content)[0]), 24)
    
    def test_delete_account(self):
        self.buyer_user()
        url = reverse('api:review') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        # Checking there are two users, each with 24 items
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(len(json.loads(response.content)[0]), 37)

    def test_delete_account(self):
        self.buyer_user()
        url = reverse('api:delete account', kwargs={
            'user' : 1
        }) 
        response = self.client.delete(url) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(id=1).exists(), False)

    def test_update_details(self):
        self.buyer_user()
        
        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'theme'}) 
        response = self.client.put(url, data=json.dumps('light'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).theme_preference, 'light')
        
        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'currency'}) 
        response = self.client.put(url, data=json.dumps('EUR'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).currency, 'EUR')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'mode'}) 
        response = self.client.put(url, data=json.dumps('seller'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).mode, 'seller')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'email'}) 
        response = self.client.put(url, data=json.dumps('newemail@gmail.com'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).email, 'newemail@gmail.com')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'username'}) 
        response = self.client.put(url, data=json.dumps('admin1'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).username, 'admin1')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'password'}) 
        response = self.client.put(url, data=json.dumps('password123'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).check_password('password123'), True)

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'name'}) 
        response = self.client.put(url, data=json.dumps('newname'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).first_name, 'newname')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'surname'}) 
        response = self.client.put(url, data=json.dumps('surname'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).last_name, 'surname')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'number'}) 
        response = self.client.put(url, data=json.dumps('0712345683'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).phone_number, '0712345683')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'description'}) 
        response = self.client.put(url, data=json.dumps('A new updated description.'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=1).description, 'A new updated description.')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'address_line_one'}) 
        response = self.client.put(url, data=json.dumps('new line one'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Address.objects.get(user__id=1).first_line, 'new line one')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'address_line_two'}) 
        response = self.client.put(url, data=json.dumps('new line two'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Address.objects.get(user__id=1).second_line, 'new line two')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'city'}) 
        response = self.client.put(url, data=json.dumps('new city'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Address.objects.get(user__id=1).city, 'new city')

        url = reverse('api:details', kwargs={'id' : 1,'attribute' : 'postcode'}) 
        response = self.client.put(url, data=json.dumps('new post'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Address.objects.get(user__id=1).postcode, 'new post')

        url = reverse('api:details', kwargs={'id' : 1, 'attribute' : 'subjects'}) 
        response = self.client.put(url, data=json.dumps('English'), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Subject.objects.filter(user__id=1, name='English').exists())
        # Delete subject
        response = self.client.delete(url, data=json.dumps(1), content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subject.objects.filter(user__id=1, name='English').exists())

    def test_check_details_email(self):
        self.buyer_user()
        url = reverse('api:check details', kwargs={
            'id' : 1,
            'attribute' : 'email'
        }) 
        response = self.client.put(url,
            data=json.dumps(TEST_EMAIL),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)
        response = self.client.put(url,
            data=json.dumps('nonexistentemail@gmail.com'),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
    
    def test_check_details_username(self):
        self.buyer_user()
        url = reverse('api:check details', kwargs={
            'id' : 1,
            'attribute' : 'username'
        }) 
        response = self.client.put(url,
            data=json.dumps(TEST_USERNAME),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)
        response = self.client.put(url,
            data=json.dumps('nonexistentusername'),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
    
    def test_check_details_number(self):
        self.buyer_user()
        url = reverse('api:check details', kwargs={
            'id' : 1,
            'attribute' : 'number'
        }) 
        response = self.client.put(url,
            data=json.dumps(TEST_PHONE_NUMBER),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)
        response = self.client.put(url,
            data=json.dumps('0711111118'),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
    
    def test_check_details_password(self):
        self.buyer_user()
        url = reverse('api:check details', kwargs={
            'id' : 1,
            'attribute' : 'password'
        }) 
        response = self.client.put(url,
            data=json.dumps(TEST_PASSWORD),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), True)
        response = self.client.put(url,
            data=json.dumps('nfdsd'),
            content_type='application/json'
        ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), False)
    
    def test_resources(self):
        self.buyer_user()
        url = reverse('api:resources') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        # Checking there are two users, each with 24 items
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(len(json.loads(response.content)[0]), 37)

    def test_resources(self):
        self.buyer_user()
        url = reverse('api:resources') 
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        # Checking there are two users, each with 24 items
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(len(json.loads(response.content)[0]), 37)