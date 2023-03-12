from django.contrib.auth.models import AbstractUser, Permission, _user_get_permissions
from django.db import models

from user_role.managers import UserManager, RoleManager
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    objects = RoleManager()

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name,


class User(AbstractUser):
    username = None
    groups = None
    role = models.ForeignKey(
        Role,
        verbose_name=_("role"),
        blank=True,
        null=True,
        help_text=_(
            "This user's role."
            "The user has all the permissions granted by the role."
        ),
        related_name="user",
        on_delete=models.SET_NULL
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_role_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        role. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "role")
