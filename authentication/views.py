from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.conf import settings


# Create your views here.
def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username +' you are now logged in')
                    return redirect(settings.LOGIN_REDIRECT_URL)
                messages.error(request, 'Account is not active,please check your email')
                return render(request, 'auth/login.html')
            messages.error(request, 'Invalid credentials,try again')
            return render(request, 'auth/login.html')
        messages.error(request, 'Please fill all fields')
        return render(request, 'auth/login.html')
    else:
        return render(request, 'auth/login.html')

def register(request):
    if (request.method == 'POST'):
        username = request.POST.get('uname')
        # fname = request.POST.get('fname')
        # lname = request.POST.get('lname')
        fname = username
        lname = username
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        context = {
            'fieldValues': request.POST
        }

        if password and cpassword and password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html', context)
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'auth/register.html', context)
                
                user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
                user.set_password(password)
                user.save()
                messages.success(request, 'Register success')
                return render(request, 'auth/register.html')
    else:
        return render(request, 'auth/register.html')

def logout(request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/')
        # return redirect('login')

def forgotPassword(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        if email:
            if User.objects.filter(email=email).exists():
                return redirect('check_email')
            messages.error(request, 'Account is not active,please check your email')
            return render(request, 'auth/forgot_password.html')
        messages.error(request, 'Invalid credentials,try again')
        return render(request, 'auth/forgot_password.html')
    else:
        return render(request, 'auth/forgot_password.html')
    
def checkEmail(request):
    return render(request, 'auth/check_email.html')
        