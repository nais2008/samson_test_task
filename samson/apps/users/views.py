import datetime

import django.contrib.auth.decorators
import django.contrib.auth.models
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.utils.timezone
from django.utils.translation import gettext_lazy as _

import apps.users.forms

__all__ = ["profile", "signup", "activate", "activate"]


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"

    form = apps.users.forms.UserProfileForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=request.user,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        return django.shortcuts.redirect("users:profile")

    context = {
        "title": _("Samson | Profile"),
        "user": request.user,
        "form": form,
    }

    return django.shortcuts.render(request, template, context)


def signup(request):
    template = "users/signup.html"

    form = apps.users.forms.UserCreationForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        user = form.save(active=django.conf.settings.DEFAULT_USER_IS_ACTIVE)
        link = request.build_absolute_uri(
            django.urls.reverse(
                "users:activate",
                args=[user.id],
            ),
        )
        django.core.mail.send_mail(
            f"Активация учетной записи, {user.username}",
            f"{link}\n{user.username}",
            django.conf.settings.MAIL,
            [user.email],
            fail_silently=False,
        )
        django.contrib.messages.success(
            request,
            (
                _(
                    "Account Activation Link sent to the specified email",
                ),
            ),
        )

        return django.shortcuts.redirect("users:signup")

    if request.method == "POST":
        django.contrib.messages.error(
            request,
            (_("There was an error submitting the form.")),
        )

    context = {
        "title": _("SAMSON | SignUp"),
        "form": form,
    }

    return django.shortcuts.render(
        request,
        template,
        context,
    )


def activate(request, pk):
    model = django.contrib.auth.models.User
    user = model.objects.get(pk=pk)
    if (
        user.date_joined + datetime.timedelta(hours=12)
        > django.utils.timezone.now()
    ):
        user.is_active = True
        user.save()

    return django.shortcuts.redirect("homepage:homepage")


def reactivate(request, pk):
    model = django.contrib.auth.models.User
    user = model.objects.get(pk=pk)
    if (
        user.block_date + datetime.timedelta(days=7)
        > django.utils.timezone.now()
    ):
        user.is_active = True
        user.save()

    return django.shortcuts.redirect("homepage:homepage")
