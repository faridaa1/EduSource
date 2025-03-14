from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Specifying app name and primary key field"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
