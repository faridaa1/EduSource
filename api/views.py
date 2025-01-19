from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import SignupForm, AddressForm

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        signup_form: SignupForm = SignupForm(request.POST)
        address_form: AddressForm = AddressForm(request.POST)
        if SignupForm(request.POST).is_valid() and AddressForm(request.POST).is_valid():
            pass
        else:
            return render(request, 'api/signup.html', {'signup_form' : signup_form, 'address_form' : address_form})
    return render(request, 'api/signup.html', {'signup_form' : SignupForm(), 'address_form' : AddressForm()})