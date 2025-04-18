from django.test import Client, TestCase
from django.urls import reverse

from api.models import User

TEST_USERNAME = 'farida'
TEST_PASSWORD = 'farida123'

class UserTestCase(TestCase):
    """Testing user signup and login"""
    def setUp(self):
        self.client = Client()
        user = User.objects.create(username=TEST_USERNAME)
        user.set_password(TEST_PASSWORD)
        user.save()
    
    def test_signup(self):
        url = reverse('api:signup')
        print(url)