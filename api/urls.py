from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import signup, login, currency_conversion, user, resources, user_details, check_details, new_listing

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/currency-conversion/<str:from_currency>/<str:price>/<str:to_currency>/', currency_conversion, name='currency conversion'),
    path('api/user/', user, name='user'),
    path('api/resources/', resources, name='resources'),
    path('api/user/<int:id>/new-listing/', new_listing, name='new listing'),
    path('api/user/<int:id>/<str:attribute>/', user_details, name='details'),
    path('api/user/<int:id>/check/<str:attribute>/', check_details, name='check details'),
]