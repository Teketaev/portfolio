from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']