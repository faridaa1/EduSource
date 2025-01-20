from django.urls import path
from .views import signup, login, user, user_details

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/user/', user, name='user'),
    path('api/user/<int:id>/details/', user_details, name='details')
]