from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

