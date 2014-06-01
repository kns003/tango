from django import forms

class InstagramForm(forms.Form):
	username = forms.CharField(max_length=30)