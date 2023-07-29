from django import forms
from Article.models import Article

from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='Title')
    class Meta:
        model = Article
        fields = ['title','content','series']


# Update_User_forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Old Password'}),
        label=''
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label=''
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label=''
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class UserForm(forms.ModelForm):
    username = forms.CharField(label='', help_text='', max_length=150)
    class Meta:
        model = User
        fields = ['username']  


class EmailForm(forms.ModelForm):
    email = forms.EmailField(label='',required=False)
    class Meta:
        model = User
        fields = ['email']




class SubscriptionForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    country = CountryField(max_length=2).formfield(widget=CountrySelectWidget())
    rib = forms.CharField(max_length=20)
    group = forms.CharField(widget=forms.HiddenInput(), initial='Subscribre')
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']

    picture = forms.ImageField(label='Photo de profil', required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))