from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField()
    description = forms.TextInput()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2', 'description', 'picture']
