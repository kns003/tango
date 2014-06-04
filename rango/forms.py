from django import forms
from django.contrib.auth.models import User

class InstagramForm(forms.Form):
	username = forms.CharField(max_length=30)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')