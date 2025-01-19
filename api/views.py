from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from .forms import SignupForm, AddressForm, LoginForm
from .models import User, Address

def signup(request: HttpRequest) -> HttpResponse:
    """Handling user sign up"""
    if request.method == 'POST':
        signup_form: SignupForm = SignupForm(request.POST)
        address_form: AddressForm = AddressForm(request.POST)
        if signup_form.is_valid() and address_form.is_valid():
            signup_data: dict[str: str] = signup_form.cleaned_data
            address_data: dict[str: str] = address_form.cleaned_data
            user : User = User.objects.create_user(
                email=signup_data['email'],
                first_name=signup_data['first_name'],
                last_name=signup_data['last_name'],
                phone_number=signup_data['phone_number'],
                username=signup_data['username'],
                password=signup_data['password'],
                theme_preference=signup_data['theme_preference'],
                mode=signup_data['mode'],
                description=signup_data['description']
            )
            Address.objects.create(
                first_line=address_data['first_line'],
                second_line=address_data['second_line'],
                city=address_data['city'],
                postcode=address_data['postcode'],
                user=user
            )
            # log in user
            authenticated_user: User | None = authenticate(request, username=signup_data['username'], password=signup_data['password'])
            if authenticated_user:
                auth.login(request, authenticated_user)
            return redirect('http://localhost:5173/')
        return render(request, 'api/signup.html', {'signup_form' : signup_form, 'address_form' : address_form})
    return render(request, 'api/signup.html', {'signup_form' : SignupForm(), 'address_form' : AddressForm()})


def login(request: HttpRequest) -> HttpResponse:
    """Handling user log in"""
    return render(request, 'api/login.html', {'login_form' : LoginForm()})