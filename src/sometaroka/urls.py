from django.contrib import admin
from django.urls import path
from . import views

# from rest_framework import routers
# from .views import apiTest


urlpatterns = [
    path("tests/", views.apiTest.as_view(), name="test"),
    path('translate/', views.transTest.as_view(), name='translate'),
    
    ]

# router = routers.DefaultRouter()
# router.register(r"tests", apiTest)
