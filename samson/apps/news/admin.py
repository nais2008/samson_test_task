import django.contrib.admin

import apps.news.models

__all__ = ()


class ImageInline(django.contrib.admin.TabularInline):
    model = apps.news.models.Image
    field = [
        apps.news.models.Image.image.field.name,
    ]


@django.contrib.admin.decorators.register(
    apps.news.models.News,
)
class NewsAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (apps.news.models.News.data.field.name,)
    list_display = (
        apps.news.models.News.title.field.name,
        apps.news.models.News.data.field.name,
        apps.news.models.News.image_tmb,
    )
    list_display_links = (apps.news.models.News.title.field.name,)
    inlines = (ImageInline,)
