from django.forms import RadioSelect
from django.apps import apps
from django.conf import settings


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
            subgroup = {}
            for _, options, _ in _groups:
                for option in options:
                    content_type = option['value'].instance.content_type
                    _app_model = f"{content_type.app_label}.{content_type.model}"
                    if _app_model in app_model:
                        group[1].append(option)
            group_index += 1
            groups.append(group)
        self._make_subgroups(groups)
        return groups

    def _make_subgroups(self, groups):
        for index, (_, options, _) in enumerate(groups):
            subgroup = {}
            for option in options:
                content_type = option['value'].instance.content_type
                model_label = content_type.model_class()._meta.verbose_name.title()
                if model_label in subgroup:
                    subgroup[model_label].append(option)
                else:
                    subgroup[model_label] = [option]
            subgroup = [{"name": name_group, "options": opts} for name_group, opts in subgroup.items()]
            groups[index][1] = subgroup

    def get_groups_permissions(self):
        if self.groups_permissions:
            return self.groups_permissions
        groups_permissions = self._get_group_permissions_from_project()
        print(groups_permissions)
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
        for key in settings.PERMISSIONS_LABELS:
            if option["value"].instance.codename.startswith(key):
                option["label"] = settings.PERMISSIONS_LABELS[key]
        return option

    class Media:
        css = {
            "all": ("permissions.css",)
        }
        js = ("permissions.js",)