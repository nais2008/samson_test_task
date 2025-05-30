import django.apps
from django.utils.translation import gettext_lazy as _

__all__ = ["DownloadConfig"]


class DownloadConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.download"
    verbose_name = _("Download")
