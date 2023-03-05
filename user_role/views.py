from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import render


class LoginView(AuthLoginView):
    form_class = AuthenticationForm
