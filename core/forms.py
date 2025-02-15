from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PASSENGER 

class PassengerRegistrationForm(UserCreationForm): 
    email = forms.EmailField(required=True)

    class UX_FORM: 
        model = PASSENGER
        fields = ["username", "email", "password1", "password2"]

class LoginPage(AuthenticationForm): 
    username = forms.Charfield(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))