from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .forms import SignupForm, AddressForm

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        signup_form: SignupForm = SignupForm(request.POST)
        address_form: AddressForm = AddressForm(request.POST)
        if SignupForm(request.POST).is_valid() and AddressForm(request.POST).is_valid():
            print('valid') 
            return redirect('http://localhost:5173/')
        else:
            return render(request, 'api/signup.html', {'signup_form' : signup_form, 'address_form' : address_form})
    return render(request, 'api/signup.html', {'signup_form' : SignupForm(), 'address_form' : AddressForm()})