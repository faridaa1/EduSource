from django.urls import path
from .views import signup, login, user, user_details, check_details

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/user/', user, name='user'),
    path('api/user/<int:id>/<str:attribute>/', user_details, name='details'),
    path('api/user/<int:id>/check/<str:attribute>/', check_details, name='check details')
]