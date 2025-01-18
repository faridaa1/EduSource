from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import SignupForm, AddressForm

# Create your views here.
def signup(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/signup.html', {'form1' : SignupForm(), 'form2' : AddressForm()})