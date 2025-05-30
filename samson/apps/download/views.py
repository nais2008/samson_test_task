import django.conf
import django.http

__all__ = ["download_image"]


def download_image(request, image_path):
    return django.http.FileResponse(
        open(django.conf.settings.MEDIA_ROOT / image_path, "rb"),
        as_attachment=True,
    )
