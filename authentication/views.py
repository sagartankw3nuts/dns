from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _

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

                subject = 'DNSDAD Reset Password'
                template_name = 'email/reset-password.html'
                context = {
                    'heading': 'This is a heading',
                    'message': 'This is a paragraph.',
                }
                from_email = settings.EMAIL_HOST_USER
                to_email = [email] 

                html_message = render_to_string(template_name, context)

                send_mail(subject, '', from_email, to_email, html_message=html_message)

                return redirect('check_email')
            messages.error(request, 'Account is not active,please check your email')
            return render(request, 'auth/forgot_password.html')
        messages.error(request, 'Invalid credentials,try again')
        return render(request, 'auth/forgot_password.html')
    else:
        return render(request, 'auth/forgot_password.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'auth/forgot_password.html'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                        "if an account exists with the email you entered. You should receive them shortly." \
                        " If you don't receive an email, " \
                        "please make sure you've entered the address you registered with, and check your spam folder."
    # success_url = reverse_lazy('users-home')

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    post_reset_login = True
    # extra_context = {'custom_message': _('Enter your new password.')}

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.post_reset_login:
            # Obtain the user from the form instance
            # user = form.user
            # Log the user in
            return redirect(settings.LOGIN_REDIRECT_URL)

def checkEmail(request):
    return render(request, 'auth/check_email.html')
        