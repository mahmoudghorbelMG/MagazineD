from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm


# Define the SignupForm
class SignupForm(UserCreationForm):

    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        #captcha = CaptchaField(label="")

    # Define a custom clean_username method to validate the username field
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        return username

    # Define a custom clean_email method to validate the email field
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Cet email est déjà utilisé. Veuillez en saisir un autre.")
        return email

    # Define a custom clean method to validate the form as a whole
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if the password and confirm password fields match
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password Doesn't Much")
        return cleaned_data


# Define the LoginForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label="")
    password = forms.CharField(widget=forms.PasswordInput, label="")
    # captcha = CaptchaField(label="")
