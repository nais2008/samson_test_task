import django.urls

import apps.homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path(
        "",
        apps.homepage.views.home,
        name="homepage",
    ),
]
