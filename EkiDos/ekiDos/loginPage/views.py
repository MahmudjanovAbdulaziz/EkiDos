from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .forms import *  
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect


def loginview(request):
    return HttpResponse('Страница Логина')

class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'loginPage/registration.html'
    success_url = reverse_lazy('loginPage:loginView')

    def form_valid(self, form):
        return super().form_valid(form)

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'loginPage/login.html'


    def get_success_url(self):
        return reverse_lazy('mainPage:index')