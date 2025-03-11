from django.contrib import admin
from .models import Cart, CartResource, Exchange, Messages, Order, OrderResource, Resource, Review, SearchHistory, SearchHistoryItem, Subject, User, Address, Message
from django.forms import BaseInlineFormSet, ValidationError


class AddressInlineFormSet(BaseInlineFormSet):
    """Ensures user enters Address"""
    def clean(self):
        super().clean()

        for form in self.forms:
            if not form.cleaned_data:
                raise ValidationError('Address is required')


class AddressInline(admin.StackedInline):
    """Defining Address model appearance on django admin"""
    model = Address
    formset = AddressInlineFormSet


class ResourceInline(admin.StackedInline):
    """Defining Resource model appearance on User page on django admin"""
    model = Resource
    extra = 0


class ReviewInline(admin.StackedInline):
    """Defining Review model appearance on Resource page on django admin"""
    model = Review
    extra = 0


class UserInline(admin.StackedInline):
    """Defining User model appearance on Cart page on django admin"""
    model = User
    extra = 0


class SubjectInline(admin.StackedInline):
    """Defining Subject model appearance on django admin"""
    model = Subject
    extra = 0


class OrderResourceInline(admin.StackedInline):
    """Defining OrderResource model appearance on Order page django admin"""
    model = OrderResource
    extra = 0


class SearchHistoryItemInline(admin.StackedInline):
    """Defining OrderResource model appearance on SearchHistory page django admin"""
    model = SearchHistoryItem
    extra = 0


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """Defining Exchange model appearance on django admin"""
    list_display: tuple[str] = ('id', 'user')
    inlines = [SearchHistoryItemInline]


class MessageInline(admin.StackedInline):
    """Defining Message model appearance on Messages page django admin"""
    model = Message
    extra = 0


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    """Defining Exchange model appearance on django admin"""
    list_display: tuple[str] = ('id', 'user1', 'user2', 'resource1', 'resource2')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Defining Order model appearance on django admin"""
    list_display: tuple[str] = ('id', 'buyer', 'seller', 'status', 'estimated_delivery_date')
    inlines = [OrderResourceInline]


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    """Defining Messages model appearance on django admin"""
    list_display: tuple[str] = ('id', 'user1', 'user2')
    inlines = [MessageInline]


class CartResourceInline(admin.StackedInline):
    """Defining CartResource model appearance on Cart page django admin"""
    model = CartResource
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Defining Cart model appearance on django admin"""
    list_display: tuple[str] = ('items', 'total')
    inlines = [CartResourceInline, UserInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Defining Resource model appearance on django admin"""
    list_display: tuple[str] = ('id', 'name', 'author', 'type')
    inlines = [ReviewInline,]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Defining User model appearance on django admin"""
    list_display: tuple[str] = ('first_name', 'last_name', 'email')
    inlines = [SubjectInline, AddressInline, ResourceInline]


