from django.contrib.auth.backends import ModelBackend as AuthModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Exists, OuterRef, Q

UserModel = get_user_model()


class ModelBackend(AuthModelBackend):

    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_role_permissions(self, user_obj):
        return user_obj.role.permissions.all()

    def get_role_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, "role")

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, "_perm_cache"):
            user_obj._perm_cache = {
                *self.get_user_permissions(user_obj, obj=obj),
                *self.get_role_permissions(user_obj, obj=obj),
            }
        return user_obj._perm_cache