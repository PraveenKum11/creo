from django import forms
from django.core.validators import MinLengthValidator

# Simple forms
class Login(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput)

class Register(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput, \
        required=True,
        validators=(
            MinLengthValidator(5),
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput, \
        required=False, \
        validators=(
            MinLengthValidator(5),
    ))
