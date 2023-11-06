
from django.urls import path
from . import views

# from rest_framework import routers
# from .views import apiTest


urlpatterns = [
  
    path('translate/',views.translate_text_osaka),
]

# router = routers.DefaultRouter()
# router.register(r"tests", apiTest)
