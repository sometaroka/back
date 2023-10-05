from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.SometarokaView.as_view(),name='home'),
    path('login/',views.MyLoginView.as_view(),name='login'),
    path('signup/',views.MySignupView.as_view(),name='signup'),
]