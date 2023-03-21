from django import forms
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from core.widgets import PermissionsSelectMultiply
from user_role.models import Role


class RoleCreationForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        label=_("Permissions"),
        widget=PermissionsSelectMultiply(),
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Role
        fields = [
            "name",
            "permissions"
        ]
