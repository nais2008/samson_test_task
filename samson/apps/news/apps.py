import django.apps
from django.utils.translation import gettext_lazy as _


class NewsConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.news"
    verbose_name = _("News")
