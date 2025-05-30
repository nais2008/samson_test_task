import django.urls

import apps.download.views

app_name = "download"

urlpatterns = [
    django.urls.path(
        "<path:image_path>/",
        apps.download.views.download_image,
        name="download_image",
    ),
]
