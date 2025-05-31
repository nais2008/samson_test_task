import django.urls

import apps.news.views

app_name = "news"

urlpatterns = [
    django.urls.path(
        "",
        apps.news.views.news_list,
        name="news-list",
    ),
    django.urls.path(
        "<int:news_pk>/",
        apps.news.views.news_detail,
        name="news"
    ),
    django.urls.path(
        "search/",
        apps.news.views.search,
        name="search",
    ),
    django.urls.path(
        "create/",
        apps.news.views.create_news,
        name="create",
    ),
    django.urls.path(
        "<int:news_pk>/update/",
        apps.news.views.update_news,
        name="update",
    ),
    django.urls.path(
        "<int:news_pk>/delete/",
        apps.news.views.delete_news,
        name="delete",
    ),
]
