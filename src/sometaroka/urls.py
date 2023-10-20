# from django.urls import path
# from . import views


# urlpatterns = [
#     path('home/',views.SometarokaView.as_view(),name='home'),
#     path('login/',views.MyLoginView.as_view(),name='login'),
#     path('signup/',views.MySignupView.as_view(),name='signup'),
# ]

from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.SometarokaView.as_view(), name='home'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('api/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]
