from user_role.widgets import PermissionsSelectMultiply as AuthPermissionsSelectMultiply


class PermissionsSelectMultiply(AuthPermissionsSelectMultiply):
    groups_permissions = {
        "Безопасность": ["user_role.role", "core.user"]
    }
