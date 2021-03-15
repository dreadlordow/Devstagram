from django.contrib.auth import views as auth_views, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from devstagram.registration.forms import RegisterForm


class RegisterView(views.CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return self.success_url


class SignInView(auth_views.LoginView):
    template_name = 'registration/login.html'


class SignOutView(auth_views.LogoutView):
    redirect_field_name = reverse_lazy('landing page')