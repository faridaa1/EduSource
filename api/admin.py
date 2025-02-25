from django.contrib import admin
from .models import Cart, CartResource, Messages, Order, OrderResource, Resource, Review, User, Address
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
    model = Resource
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class UserInline(admin.StackedInline):
    model = User
    extra = 0


class OrderResourceInline(admin.StackedInline):
    model = OrderResource
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Defining Order model appearance on django admin"""
    list_display: tuple[str] = ('id', 'status', 'estimated_delivery_date')
    inlines = [OrderResourceInline]


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    """Defining Messages model appearance on django admin"""
    list_display: tuple[str] = ('id', 'user1', 'user2')


class CartResourceInline(admin.StackedInline):
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
    list_display: tuple[str] = ('name', 'author', 'type')
    inlines = [ReviewInline,]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Defining User model appearance on django admin"""
    list_display: tuple[str] = ('first_name', 'last_name', 'email')
    inlines = [AddressInline, ResourceInline]


