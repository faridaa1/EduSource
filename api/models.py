from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Defining attrbiutes and methods for User model"""
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    last_name = models.CharField(max_length=150, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    phone_number = models.CharField(max_length=11 ,unique=True, null=False, blank=False, validators=[RegexValidator(r'^07(\d{8,9})$', message='Must be 10 or 11 digit number starting with 07')])
    rating = models.FloatField(null=False, blank=True, default=0.0)
    description = models.TextField(null=False, blank=True, validators=[RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    THEMES: list [tuple[str, str]] = [('light', 'light'), ('dark', 'dark')]
    theme_preference = models.CharField(max_length=5, choices=THEMES, default='light', null=False, blank=False)
    
    MODES: list [tuple[str, str]] = [('buyer', 'buyer'), ('seller', 'seller')]
    mode = models.CharField(max_length=6, choices=MODES, default='buyer', null=False, blank=False)
    
    CURRENCIES: list [tuple[str, str]] = [('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')]
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='GBP', null=False, blank=False)

    groups = models.ManyToManyField(Group, blank=True, related_name='new_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='new_user_permissions_set')

    def __str__(self) -> str:
        """Defining string representation of User model"""
        return f"{self.first_name} {self.last_name}: {self.email}"
    
    def as_dict(self) -> dict[str, int | float | str]:
        """Dictionary representation of User object"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'rating': self.rating,
            'description': self.description,
            'theme_preference': self.theme_preference,
            'mode': self.mode,
            'currency': self.currency
        }

class Address(models.Model):
    """Defining attributes and methods for Address model"""
    first_line = models.CharField(max_length=255, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z0-9 ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    second_line = models.CharField(max_length=255, null=False, blank=True, validators=[RegexValidator(r'^[a-zA-Z0-9 ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    city = models.CharField(max_length=255, null=False, blank=False, validators=[RegexValidator(r'^[a-zA-Z0-9 ]+$', message='No special characters allowed'), RegexValidator(r'^\S+( \S+)*$', message='Only one space between words')])
    postcode = models.CharField(max_length=7, null=False, blank=False, validators=[RegexValidator(r'^[A-Za-z0-9]{5,7}$', message='Enter 5-7 character postcode without spaces')])
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    
    def __str__(self) -> str:
        """Defining string representation of Address model"""
        return f"{self.first_line} {self.city} {self.postcode}"