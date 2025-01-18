from django import forms
from django.forms import ModelForm
from api.models import User, Address

class AddressForm(ModelForm):
    class Meta:
        model: Address = Address
        fields: list[str, str] = [
            'first_line',
            'second_line',
            'city',
            'postcode'
        ]
        

class SignupForm(ModelForm):
    """Form used for signing up a user"""
    class Meta:
        model: User = User
        fields: list[str] = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'password',
            'theme_preference',
            'mode',
            'description',
        ]
        # fields_classes: dict[str, any] = {
        #     'password' : PasswordField
        # }
        labels: dict[str, str] = {
            # 'email' : 'Email', 
            # 'first_name' : 'First Name' 
        }
    
    def __init__(self) -> None:
        super(SignupForm, self).__init__()
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class' : 'form-control',
                    'placeholder' : field
                }
            )