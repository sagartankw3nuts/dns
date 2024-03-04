from django.urls import path
from . import views

urlpatterns = [
    path('sign-in', views.login, name='sign_in'),
    path('sign-up', views.register, name='sign_up'),
    path('logout', views.logout, name='logout'),
    path('forgot-password', views.forgotPassword, name='forgot_password'),
    path('check-email', views.checkEmail, name='check_email'),
]