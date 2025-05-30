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
]
