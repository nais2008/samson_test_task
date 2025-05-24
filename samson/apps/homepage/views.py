import django.shortcuts

__all__ = ["home"]


def home(request):
    template = "homepage/main.html"
    context = {
        "title": "SAMSON | Homepage",
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )
