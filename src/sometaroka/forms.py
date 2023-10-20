from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Users

class LoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = ['username','password']

class SignupForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['email','password1','password2']
