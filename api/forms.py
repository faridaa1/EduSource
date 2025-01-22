import re
from django import forms
from django.forms import ModelForm, ValidationError
from django.core.validators import validate_email
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

    def clean_username(self) -> ValidationError | str:
        """Handling username validation"""
        username: str = self.cleaned_data['username']
        if not re.match(r"^[a-zA-Z0-9]+$", username):
            if re.search(r"\s", username):
                raise ValidationError('Username cannot contain spaces')
            raise ValidationError('Username cannot contain special characters')
        return username
    
    def clean_description(self) -> ValidationError | str:
        """Handling description validation"""
        mode: str = self.cleaned_data['mode']
        if mode == 'buyer':
            return ''
        description: str = self.cleaned_data['description']
        return description
    
    def clean_password(self) -> ValidationError | str:
        """Handling password validation"""
        password: str = self.cleaned_data['password']
        username: str | None = self.cleaned_data.get('username', None)
        email: str | None = self.cleaned_data.get('email', None)
        if re.search(r"\s", password):
            raise ValidationError('Password cannot contain spaces')
        if len(password) < 8 or len(password) > 15:
            raise ValidationError('Password must be between 8 to 15 characters long')
        if username == password:
            raise ValidationError('Password cannot be the same as username')
        if password == email:
            raise ValidationError('Password cannot be the same as email')
        return password
    
    def clean_reenter_password(self) -> ValidationError | str:
        """Handling re-entered password validation"""
        reentered_password: str = self.cleaned_data['reenter_password']
        clean_password: str | None = self.cleaned_data.get('password', None)
        if clean_password and not self.cleaned_data['password'] == reentered_password:
                raise ValidationError('Both passwords must match')
        return reentered_password
    

class LoginForm(ModelForm):
    """Form used for logging in a user"""
    user = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model: User = User
        fields: list[str, str] = [
            'user',
            'password',
        ]

    def __init__(self, *args, **kwargs) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                    'class' : 'form-control',
                    'placeholder' : field
                }
            )

    def clean_user(self) -> ValidationError | str:
        """Handling username validation"""
        username: str = self.cleaned_data['user']
        if '@' in username:
            """Handle like email"""    
            validate_email(username)
        else:
            """Handle like username"""  
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