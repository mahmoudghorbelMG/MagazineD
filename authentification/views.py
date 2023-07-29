from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .my_captcha import FormWithCaptcha
from django.views.decorators.cache import never_cache
from Article.models import Article
from Magazine.views import Home


import random

def generate_username(name, fname):
    """Generate a unique username based on the name and first name."""
    username = f"{name}{fname}"
    suffix = random.randint(100, 999)  # Add a random number suffix to the username.
    return f"{username}{suffix}"

def sign_in_or_up(request):
    if request.method == "POST":
        if 'signup' in request.POST:
            name = request.POST.get('name')
            fname = request.POST.get('fname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken.")
                return redirect('sign')
            # Check if the password and confirm password fields match
            if password != cpassword:
                messages.error(request, "Passwords do not match.")
                return redirect('sign')
            # Generate a username based on the name and first name.
            username = generate_username(name, fname)
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect('sign')
            verification_code = generate_verification_code()
            send_verification_code(email, verification_code)
            # Save the user's data and the verification code in the session
            request.session['name'] = name
            request.session['fname'] = fname
            request.session['email'] = email
            request.session['password'] = password
            request.session['verification_code'] = verification_code
            # Render the verification page
            return redirect('verify')
        elif 'signin' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                user = authenticate(request=request, email=email, password=password, backend='Athena.backends.EmailBackend')
                if user is not None:
                    login(request, user)
                    return redirect('Home')
                else:
                    messages.error(request, "Username or password is incorrect. Please try again.")
                    form = FormWithCaptcha(request.POST)
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
                return render(request, 'sign.html', {"captcha": form,
                                                      "signin_error": messages.get_messages(request),"signup_error": messages.get_messages(request)})
    # Render the sign-in/sign-up page
    form = FormWithCaptcha()
    return render(request, 'sign.html', {"captcha": form})

@login_required
@never_cache
def logout_view(request):
    logout(request)
    response = redirect('Home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


import random
import string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail


def generate_verification_code():
    # Generate a random string of 6 characters
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_verification_code(email, code):
    # Send an email to the user with the verification code
    subject = 'Verification Code'
    message = f'Your verification code is {code}'
    from_email = 'noreply@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify(request):
    if request.method == "POST":
        input1 = request.POST.get('input1')
        input2 = request.POST.get('input2')
        input3 = request.POST.get('input3')
        input4 = request.POST.get('input4')
        input5 = request.POST.get('input5')
        input6 = request.POST.get('input6')
        entered_code = input1+input2+input3+input4+input5+input6
        expected_code = request.session.get('verification_code')

        if entered_code == expected_code:
            name = request.session.get('name')
            fname = request.session.get('fname')
            email = request.session.get('email')
            password = request.session.get('password')
            # Create a new user object and save it to the database
            username = generate_username(name, fname)
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.last_name = fname
            user.save()
            # Log in the user
            user = authenticate(request=request, email=email, password=password, backend='Athena.backends.EmailBackend')
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "Invalid verification code. Please try again.")
            return render(request, 'verification.html', {'email': request.session.get('email')})
    # Render the verification page
    return render(request, 'verification.html', {'email': request.session.get('email')})