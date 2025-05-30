import django.shortcuts
from django.utils.translation import gettext_lazy as _

import apps.news.models

__all__ = ["news_list", "news_detail"]


def news_list(request):
    template = "news/news_list.html"
    news = apps.news.models.News.objects.by_create_at()

    context = {
        "title": _("SAMSON | News"),
        "news": news,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def news_detail(request, news_pk):
    template = "news/news_detail.html"
    news = django.shortcuts.get_object_or_404(
        apps.news.models.News.objects.detail(),
        pk=news_pk,
    )

    context = {
        "title": _("SAMSON | News detail"),
        "news": news,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )
