from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from api.models import User

TEST_USERNAME = 'farida'
TEST_PASSWORD = 'farida123'

class UnitTesting(TestCase):
    """Comprehensive unit testing"""
    def setUp(self):
        self.client = Client()
        user = User.objects.create(username=TEST_USERNAME)
        user.set_password(TEST_PASSWORD)
        user.save()
    
    def test_signup(self):
        url = reverse('api:signup')
        print(url)

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
