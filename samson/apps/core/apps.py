import django.apps
from django.utils.translation import gettext_lazy as _

__all__ = ["CoreConfig"]


class CoreConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = _("Core")
