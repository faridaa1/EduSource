from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import signup, login, users, edit_review, currency_conversion, user, review, resources, user_details, check_details, new_listing, sentiment_analysis, update_cart, get_cart

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('api/users/', users, name='users'),
    path('api/currency-conversion/<int:id>/<str:from_currency>/<str:to_currency>/', currency_conversion, name='currency conversion'),
    path('api/user/', user, name='user'),
    path('api/resources/', resources, name='resources'),
    path('api/user/<int:id>/new-listing/', new_listing, name='new listing'),
    path('api/user/<int:user>/review/<int:resource>/', review, name='review'),
    path('api/user/<int:user>/edit-review/<int:id>/<int:resource>/', edit_review, name='edit review'),
    path('api/user/<int:id>/<str:attribute>/', user_details, name='details'),
    path('api/user/<int:id>/check/<str:attribute>/', check_details, name='check details'),
    path('api/sentiment/<str:resource>/', sentiment_analysis, name='sentiment analysis'),
    path('api/update-cart/<int:user>/resource/<int:resource>/', update_cart, name='update cart'),
    path('api/cart/<int:user>/', get_cart, name='get cart'),
]