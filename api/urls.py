from django.urls import path
from .views import signup, login, user

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/user/', user, name='user')
]