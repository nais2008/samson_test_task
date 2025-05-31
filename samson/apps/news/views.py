import django.contrib.auth.decorators
import django.forms
import django.http
import django.shortcuts
from django.utils.translation import gettext_lazy as _

import apps.news.forms
import apps.news.models

__all__ = ["news_list", "news_detail"]


def news_list(request):
    template = "news/news_list.html"

    context = {
        "title": _("SAMSON | News"),
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


def search(request):
    template = "news/news_list_query.html"

    query = request.GET.get("search", "")
    news = apps.news.models.News.objects.by_title_or_about(query)

    context = {
        "news": news,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def create_news(request):
    if request.method not in ["GET", "POST"]:
        return django.http.HttpResponseNotAllowed(["GET", "POST"])

    template = "news/create.html"

    NewsFormSet = django.forms.modelformset_factory(
        model=apps.news.models.News,
        form=apps.news.forms.NewsForm,
        extra=1,
        can_delete=False,
    )

    if request.method == "POST":
        formset = NewsFormSet(
            request.POST,
            request.FILES,
            queryset=apps.news.models.News.objects.none(),
        )

        if formset.is_valid():
            saved_instances = []
            for form in formset:
                if form.has_changed() and form.cleaned_data:
                    news_instance = form.save(commit=True, user=request.user)
                    saved_instances.append(news_instance)

            if saved_instances:
                django.contrib.messages.success(
                    request,
                    django.utils.translation.gettext("All news were created successfully."),
                )
                return django.shortcuts.redirect("news:news-list")

    else:
        formset = NewsFormSet(queryset=apps.news.models.News.objects.none())

    context = {
        "title": django.utils.translation.gettext("SAMSIN | Create news"),
        "formset": formset,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def update_news(request, news_pk):
    if request.method not in ["GET", "POST"]:
        return django.http.HttpResponseNotAllowed(["GET", "POST"])

    template = "news/update.html"

    news = django.shortcuts.get_object_or_404(
        apps.news.models.News,
        pk=news_pk,
    )
    try:
        image = news.image
    except apps.news.models.Image.DoesNotExist:
        image = None

    news_form = apps.news.forms.UpdateNewsForm(
        data=request.POST or None,
        instance=news,
    )
    image_form = apps.news.forms.NewsImageForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=image,
    )
    forms = (news_form, image_form)

    if request.method == "POST" and all(form.is_valid() for form in forms):
        news = news_form.save(commit=False)
        news.user = request.user
        news.save()

        image = image_form.save(commit=False)
        image.news = news
        image.save()

        django.contrib.messages.success(
            request,
            _("News update"),
        )
        return django.shortcuts.redirect("news:news-list")

    context = {
        "title": _("SAMSIN | Update news"),
        "news_form": news_form,
        "image_form": image_form,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )



@django.contrib.auth.decorators.login_required
def delete_news(request, news_pk):
    if request.method != "POST":
        return django.http.HttpResponseNotAllowed(["POST"])

    news = django.shortcuts.get_object_or_404(
        apps.news.models.News,
        pk=news_pk,
    )

    if not request.user.is_superuser:
        return django.http.HttpResponseForbidden(
            _("You are not allowed to delete this news"),
        )

    news.delete()

    django.contrib.messages.success(request, _("News successfully deleted"))
    return django.shortcuts.redirect("news:news-list")

