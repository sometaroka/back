# from django.shortcuts import render

# # Create your views here.

# from .forms import SignupForm,LoginForm
# from django.contrib.auth.views import LoginView
# from django.views.generic import TemplateView,CreateView,DeleteView,UpdateView

# class SometarokaView(TemplateView):
#     template_name = 'index.html'

# class MyLoginView(LoginView):
#     template_name = 'login.html'
#     form_class = LoginForm
#     success_url = 'home/'

# class MySignupView(CreateView):
#     template_name = 'signup.html'
#     form_class = SignupForm
#     success_url = 'home/'
    
#     def form_valid(self,form):
#         reult = super().form_valid(form)
#         user = self.object
#         login(self.request,user)
#         return result



from django.shortcuts import render
from django.contrib.auth import login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .forms import SignupForm, LoginForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, CreateView

class SometarokaView(TemplateView):
    template_name = 'index.html'

class MyLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/home/'

class MySignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = '/home/'
    
    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

class CustomTokenObtainPairView(TokenObtainPairView):
    # カスタマイズしたトークン生成のロジックが必要であれば、こちらで行う。
    pass

