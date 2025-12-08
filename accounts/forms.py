from django import forms
from .models import User

class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    username  = forms.CharField(max_length=50, min_length=3)
    email     = forms.EmailField()
    password  = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm   = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cd = super().clean()
        if cd.get('password') != cd.get('confirm'):
            raise forms.ValidationError("Passwords do not match.")
        return cd


class LoginForm(forms.Form):
    identifier    = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)