from django.urls import path
from . import views

urlpatterns = [
    path('domain-store/', views.domainStore, name='api.domain_store'),
]