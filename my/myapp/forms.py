# my/myapp/forms.py
from django import forms
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    login = forms.CharField(label="Email or Phone or Username")
    password = forms.CharField(widget=forms.PasswordInput, required=False)

class SignupForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class OTPRequestForm(forms.Form):
    phone = forms.CharField()

class OTPVerifyForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput)
    code = forms.CharField(max_length=6)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
