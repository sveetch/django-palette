"""
Sandbox URL Configuration
"""
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('', include('django_palette.urls')),
]
