import django.contrib.auth.models
import django.db.models
from django.utils.translation import gettext_lazy as _

import apps.core.models
import apps.users.email_normalizer
import apps.users.managers

__all__ = ()

normalizer = apps.users.email_normalizer.EmailNormalizer()


class User(
    django.contrib.auth.models.AbstractUser,
    apps.core.models.BaseImageModel,
):

    objects = apps.users.managers.UserManager()

    email = django.db.models.EmailField(
        _("email address"),
        unique=True,
        null=False,
        blank=False,
        help_text=_("Unique email address"),
    )
    birthday = django.db.models.DateField(
        _("birthday"),
        help_text=_("write birthday"),
        null=True,
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
