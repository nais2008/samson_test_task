import django.db.models

import apps.news.models

__all__ = ["NewsManager"]


class NewsManager(django.db.models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def by_create_at(self):
        return (
            self.select_related("image")
            .only(
                "pk",
                apps.news.models.News.title.field.name,
                apps.news.models.News.source.field.name,
                apps.news.models.News.data.field.name,
                f"image__{apps.news.models.Image.image.field.name}",
            )
            .order_by(
                f"-{apps.news.models.News.data.field.name}",
                "pk",
            )
        )

    def detail(self):
        return (
            self.select_related("image")
            .defer(
                apps.news.models.News.user.field.name,
            )
        )
