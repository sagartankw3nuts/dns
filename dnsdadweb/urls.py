from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('app-setting', views.appSettingCreate, name='app.setting'),
    path('app-create-ajax', views.appSettingStore, name='app.create'),
    path('app-file-upload', views.appFileUpload, name='app.fileupload'),
    path('app-update-secret-ajax', views.appUpdateSecret, name='app.updatesecret'),
    path('api-post-domain', views.ajaxPostDomain, name='ajax.postdomain'),
    path('billing', views.billingCreate, name='billing'),
]