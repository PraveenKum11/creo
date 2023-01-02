from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Simple forms
class Login(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

