from django.shortcuts import render
from django.views.generic import CreateView

from core.forms import RoleCreationForm


class CreateRoleView(CreateView):
    form_class = RoleCreationForm
    template_name = "role/create.html"