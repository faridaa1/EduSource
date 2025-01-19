import re
from django import forms
from django.forms import ModelForm, ValidationError
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

    def __init__(self, *args, **kwargs) -> None:
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                    'class' : 'form-control',
                    'placeholder' : field
                }
            )

    def validate_string(self, input: str) -> ValidationError | str:
        """Helper function for validating string"""
        if not re.match(r"^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$", input):
            if not re.match(r"^[a-zA-Z0-9 ]+$", input):
                raise ValidationError('No special characters allowed')
            raise ValidationError('Only one space between words')
        return input
    
    def clean_first_line(self):
        """Handling address line one validation"""
        first_line: str = self.cleaned_data['first_line']
        return self.validate_string(first_line)
    
    def clean_second_line(self):
        """Handling address line two validation"""
        second_line: str | None = self.cleaned_data.get('second_line', None)
        if second_line:
            return self.validate_string(second_line)
        return ''
    
    def clean_city(self):
        """Handling city validation"""
        city: str = self.cleaned_data['city']
        return self.validate_string(city)
    
    def clean_postcode(self):
        """Handling city validation"""
        postcode: str = self.cleaned_data['postcode'].upper()
        if not re.match(r"^[A-Z0-9]{5,7}$", postcode):
            raise ValidationError('Enter 5-7 character postcode without spaces')
        return self.validate_string(postcode)


class SignupForm(ModelForm):
    """Form used for signing up a user"""
    reenter_password = forms.CharField(max_length=15, required=True)
    class Meta:
        model: User = User
        fields: list[str] = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'username',
            'password',
            'reenter_password',
            'theme_preference',
            'mode',
            'description',
        ]
    
    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class' : 'form-control',
                    'placeholder' : field
                }
            )

    def clean_email(self) -> ValidationError | str:
        """Handling email validation"""
        email: str = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email exists')
        return email
    
    def validate_string(self, input: str) -> ValidationError | str:
        """Helper function for validating string"""
        if not re.match(r"^[a-zA-Z]+( [a-zA-Z]+)*$", input):
            if not re.match(r"^[a-zA-Z ]+$", input):
                raise ValidationError('No special characters allowed')
            raise ValidationError('Only one space between words')
        return input

    def clean_first_name(self) -> ValidationError | str:
        """Handling first name validation"""
        first_name: str = self.cleaned_data['first_name']
        return self.validate_string(first_name)
    
    def clean_last_name(self) -> ValidationError | str:
        """Handling last name validation"""
        last_name: str = self.cleaned_data['last_name']
        return self.validate_string(last_name)
    
    def clean_phone_number(self) -> ValidationError | str:
        """Handling phone number validation"""
        phone_number: str = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('An account with this phone number exists')
        if not re.match(r"^07(\d{8,9})$", phone_number):
            raise ValidationError('Must be 10 or 11 digit number starting with 07')
        return phone_number
    
    def clean_username(self) -> ValidationError | str:
        """Handling username validation"""
        username: str = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('An account with this username exists')
        if not re.match(r"^[a-zA-Z0-9]+$", username):
            if re.search(r"\s", username):
                raise ValidationError('Username cannot contain spaces')
            raise ValidationError('Username cannot contain special characters')
        return username
    
    def clean_password(self) -> ValidationError | str:
        """Handling password validation"""
        password: str = self.cleaned_data['password']
        if re.search(r"\s", password):
            raise ValidationError('Password cannot contain spaces')
        if len(password) < 8 or len(password) > 15:
            raise ValidationError('Password must be between 8 to 15 characters long')
        return password
    
    def clean_reenter_password(self) -> ValidationError | str:
        """Handling re-entered password validation"""
        reentered_password: str = self.cleaned_data['reenter_password']
        clean_password: str | None = self.cleaned_data.get('password', None)
        if clean_password:
            if not self.cleaned_data['password'] == reentered_password:
                raise ValidationError('Both passwords must match')
        return reentered_password

