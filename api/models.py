from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Address(models.Model):
    """Defining attributes and methods for Address model"""
    first_line = models.CharField(max_length=255, null=False, blank=False)
    second_line = models.CharField(max_length=255, null=False, blank=True)
    city = models.CharField(max_length=255, null=False, blank=False)
    postcode = models.CharField(max_length=255, null=False, blank=False)

class User(AbstractUser):
    """Defining attrbiutes and methods for User model"""
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=11 ,unique=True, null=False, blank=False)
    rating = models.FloatField(null=False, blank=True, default=0.0)
    description = models.TextField(null=False, blank=True)
    
    THEMES: list [tuple[str, str]] = [('light', 'light'), ('dark', 'dark')]
    theme_preference = models.CharField(max_length=5, choices=THEMES, default='light', null=False, blank=False)
    
    MODES: list [tuple[str, str]] = [('buyer', 'buyer'), ('seller', 'seller')]
    mode = models.CharField(max_length=6, choices=MODES, default='buyer', null=False, blank=False)
    
    groups = models.ManyToManyField(Group, blank=True, related_name='new_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='new_user_permissions_set')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='user')