from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from user_role.forms import RoleCreationForm
from user_role.models import Role


class LoginView(AuthLoginView):
    form_class = AuthenticationForm


class CreateRoleView(CreateView):
    form_class = RoleCreationForm
    template_name = "role/create.html"


class UpdateRoleView(UpdateView):
    model = Role
    form_class = RoleCreationForm
    template_name = "role/create.html"
