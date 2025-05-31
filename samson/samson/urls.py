import django.conf
import django.conf.urls.i18n
import django.conf.urls.static
import django.contrib
import django.urls

urlpatterns = [
    django.urls.path(
        "admin/",
        django.contrib.admin.site.urls,
    ),
    django.urls.path(
        "",
        django.urls.include("apps.homepage.urls"),
    ),
    django.urls.path(
        "download/",
        django.urls.include("apps.download.urls"),
    ),
    django.urls.path(
        "news/",
        django.urls.include("apps.news.urls"),
    ),
    django.urls.path(
        "users/",
        django.urls.include("apps.users.urls"),
    ),
]

urlpatterns += django.conf.urls.i18n.i18n_patterns(
    django.urls.path(
        "i18n/",
        django.urls.include("django.conf.urls.i18n"),
        name="set_language",
    ),
)

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.STATIC_URL,
    document_root=django.conf.settings.STATIC_ROOT,
)
urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)
