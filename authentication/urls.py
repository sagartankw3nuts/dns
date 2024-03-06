from django.urls import path
from . import views
from authentication.views import ResetPasswordView, PasswordResetConfirmView
from django.contrib.auth import views as auth_views
# from authentication. import ResetPasswordView
urlpatterns = [
    path('sign-in', views.login, name='sign_in'),
    path('sign-up', views.register, name='sign_up'),
    path('logout', views.logout, name='logout'),
    path('forgot-password', ResetPasswordView.as_view(), name='forgot_password'),
    path('password-reset-done', views.checkEmail, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
    #     name='password_reset_confirm'),
    path('password-reset-complete/',
            auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
            name='password_reset_complete'),
    
]