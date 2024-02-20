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
    path('plan', views.planList, name='plan.list'),
    path('plan-store/<int:plan_id>/', views.planStore, name='plan.store'),
    path('get_data', views.get_data, name='get_data'),
]