import django.contrib.auth
import django.db.models
from django.utils.translation import gettext_lazy as _

import apps.core.models
import apps.news.managers

__all__ = ["News"]

User = django.contrib.auth.get_user_model()


class News(django.db.models.Model):
    data = django.db.models.DateField(
        _("date created"),
        auto_now_add=True,
        help_text=_("date created"),
        null=True,
    )
    source = django.db.models.CharField(
        _("source"),
        max_length=255,
        help_text=_("Write source news"),
    )
    title = django.db.models.CharField(
        _("title"),
        max_length=512,
        help_text=_("Write title news"),
    )
    about = django.db.models.TextField(
        _("about"),
        help_text=_("Write abaout news"),
    )
    link = django.db.models.TextField(
        _("link"),
        help_text=_("Write link news"),
    )
    user = django.db.models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=django.db.models.CASCADE,
        related_name="news",
        help_text=_("user"),
    )

    objects = apps.news.managers.NewsManager()

    class Meta:
        verbose_name = _("news")
        verbose_name_plural = _("news")

    def __str__(self) -> str:
        if len(self.title) >= 25:
            return f"{self.title[:22]}..."

        return self.title

    def image_tmb(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.image.get_image_50x50.url}' />",
            )

        return _("No image or image not found")

    image_tmb.short_description = _("image")
    image_tmb.allow_tags = True


class Image(apps.core.models.BaseImageModel):
    news = django.db.models.OneToOneField(
        News,
        verbose_name=_("image"),
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = _("image news")
        verbose_name_plural = _("images news")
