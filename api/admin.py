from django.contrib import admin
from .models import User, Address
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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Defining User model appearance on django admin"""
    list_display: tuple[str] = ('first_name', 'last_name', 'email')
    inlines = [AddressInline]


