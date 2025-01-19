from django.contrib import admin
from .models import User, Address

class AddressInline(admin.StackedInline):
    model = Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ('first_name', 'last_name')
    inlines = [AddressInline]


