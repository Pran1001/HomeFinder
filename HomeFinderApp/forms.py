from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ('user', 'token', 'verify',)


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

class ImageForm(ModelForm):
    class Meta:
        model = PostImages
        fields = ("imagefile",)


class SearchForm(forms.Form):
    filter_status_by = forms.CharField(widget = forms.Select)

class FilterForm(forms.Form):
    status = forms.CharField(widget = forms.Select, required=False)
    types = forms.CharField(widget = forms.Select, required=False)
    bedroom = forms.CharField(widget = forms.Select, required=False)
    parking = forms.CharField(widget = forms.Select, required=False)
    city = forms.CharField(widget = forms.Select, required=False)
    price = forms.CharField(widget = forms.Select, required=False)

