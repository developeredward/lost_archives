from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=200)
    middle_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ["username", "profile_picture", "first_name", "middle_name",  "last_name", "email", "password1", "password2"]

