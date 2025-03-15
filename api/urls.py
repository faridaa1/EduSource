from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import order, frontend, delete_account, chatbot, order_return, feedback, signout, exchange, recommendations, submit_return, semantic_search_orders, semantic_search_subjects, semantic_search, message, messages, signup, login, users, edit_review, currency_conversion, cart_to_wishlist, user, review, resources, user_details, check_details, update_wishlist, new_listing, sentiment_analysis, update_cart, get_cart

"""Defining routing"""
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('signout/', signout, name='signout'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('delete-account/<int:user>/', delete_account, name='delete account'),
    path('api/feedback/', feedback, name='feedback'),
    path('api/chatbot/<str:user>/', chatbot, name='chatbot'),
    path('api/exchange/user/<int:user>/seller/<int:seller>/resource/<int:resource>/', exchange, name='exchange'),
    path('api/semantic-search/<str:user>/', semantic_search, name='semantic search'),
    path('api/semantic-search-subjects/', semantic_search_subjects, name='semantic search subjects'),
    path('api/semantic-search-orders/<int:id>/<str:search>/<str:mode>/', semantic_search_orders, name='semantic search orders'),
    path('api/messages/<int:user1>/<int:user2>/', messages, name='messages'),
    path('api/message/<int:id>/<int:sender>/', message, name='message'),
    path('api/users/', users, name='users'),
    path('api/recommendations/<int:user>/', recommendations, name='recommendations'),
    path('api/currency-conversion/<int:id>/<str:from_currency>/<str:to_currency>/', currency_conversion, name='currency conversion'),
    path('api/user/', user, name='user'),
    path('api/user/<int:user>/order/', order, name='order'),
    path('api/user/<int:user>/return/<int:order>/', submit_return, name='submit_return'),
    path('api/user/<int:user>/return/<int:order>/<int:resource>/', order_return, name='toggle return'),
    path('api/resources/', resources, name='resources'),
    path('api/user/<int:user>/cart-to-wishlist/', cart_to_wishlist, name='cart to wishlist'),
    path('api/user/<int:user>/wishlist/', update_wishlist, name='update wishlist'),
    path('api/user/<int:id>/new-listing/', new_listing, name='new listing'),
    path('api/user/<int:user>/review/<int:resource>/', review, name='review'),
    path('api/user/<int:user>/edit-review/<int:id>/<int:resource>/', edit_review, name='edit review'),
    path('api/user/<int:id>/<str:attribute>/', user_details, name='details'),
    path('api/user/<int:id>/check/<str:attribute>/', check_details, name='check details'),
    path('api/sentiment/<str:resource>/', sentiment_analysis, name='sentiment analysis'),
    path('api/update-cart/user/<int:user>/cart/<str:cart>/resource/<str:resource>/', update_cart, name='update cart'),
    path('api/cart/<int:user>/', get_cart, name='get cart'),
    path('', frontend, name='frontend'),
]