from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from django import forms
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.forms import RadioSelect
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst
from django.apps import apps
from user_role.models import Role

UserModel = get_user_model()


class EmailField(forms.CharField):

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "email",
        }


class UserCreationForm(AuthUserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)
        field_classes = {"email": EmailField}


class AuthenticationForm(forms.Form):
    username = EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        email_max_length = self.username_field.max_length or 254
        self.fields["email"].max_length = email_max_length
        self.fields["email"].widget.attrs["maxlength"] = email_max_length
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.username_field.verbose_name},
        )


class PermissionsSelectMultiply(RadioSelect):
    allow_multiple_selected = True
    input_type = "checkbox"
    template_name = "forms/widgets/permissions_select.html"
    option_template_name = "forms/widgets/permission_option.html"
    groups_permissions = None

    def use_required_attribute(self, initial):
        # Don't use the 'required' attribute because browser validation would
        # require all checkboxes to be checked instead of at least one.
        return False

    def value_omitted_from_data(self, data, files, name):
        # HTML checkboxes don't appear in POST data if not checked, so it's
        # never known if the value is actually omitted.
        return False

    def optgroups(self, name, value, attrs=None):
        _groups = super().optgroups(name, value, attrs)
        permissions_groups = self.get_groups_permissions()
        groups = []
        group_index = 0
        for group_name, app_model in permissions_groups.items():
            group = [group_name, [], group_index]
            for _, options, _ in _groups:
                for option in options:
                    content_type = option['value'].instance.content_type
                    _app_model = f"{content_type.app_label}.{content_type.model}"
                    if _app_model in app_model:
                        group[1].append(option)
            group_index += 1
            groups.append(group)
        return groups

    def get_groups_permissions(self):
        if self.groups_permissions:
            return self.groups_permissions
        groups_permissions = self._get_group_permissions_from_project()
        return groups_permissions

    def _get_group_permissions_from_project(self):
        groups_permissions = {}
        for permission in self.choices.queryset.all():
            content_type = permission.content_type
            app_verbose_name = apps.get_app_config(content_type.app_label).verbose_name
            if app_verbose_name not in groups_permissions:
                groups_permissions[app_verbose_name] = []
            groups_permissions[app_verbose_name].append(f"{content_type.app_label}.{content_type.model}")
        return groups_permissions

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        return option


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
