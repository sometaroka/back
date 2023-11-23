from django.contrib import admin
from django.urls import path
from . import views

# from rest_framework import routers
# from .views import apiTest


urlpatterns = [
    path("tests/", views.apiGetTest.as_view(), name="test"),
    path("talk_rooms/", views.getTalkRooms.as_view(), name="talk_rooms"),
]

# router = routers.DefaultRouter()
# router.register(r"tests", apiTest)
