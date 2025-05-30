import django.contrib.auth
import django.forms
from django.utils.translation import gettext_lazy as _

import apps.users.models

__all__ = [
    "UserCreationForm",
    "UserProfileForm",
]

normalizer = apps.users.email_normalizer.EmailNormalizer()


class UserCreationForm(
    django.contrib.auth.forms.UserCreationForm,
):
    def clean_username(self):
        username = self.cleaned_data[
            apps.users.models.User.username.field.name
        ].lower()
        if apps.users.models.User.objects.filter(username=username).exists():
            raise django.core.exceptions.ValidationError(
                _("User already exists"),
            )

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise django.core.exceptions.ValidationError(
                _("Passwords do not match"),
            )

        return password2

    def save(self, commit=True, active=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data[
            apps.users.models.User.email.field.name
        ]
        user.is_active = active

        if commit:
            user.save()

        return user

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = apps.users.models.User
        fields = (
            apps.users.models.User.username.field.name,
            apps.users.models.User.email.field.name,
            "password1",
            "password2",
        )


class UserProfileForm(
    django.contrib.auth.forms.UserChangeForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields[apps.users.models.User.password.field.name]

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = apps.users.models.User
        fields = (
            apps.users.models.User.username.field.name,
            apps.users.models.User.email.field.name,
            apps.users.models.User.first_name.field.name,
            apps.users.models.User.last_name.field.name,
            apps.users.models.User.image.field.name,
        )
        widgets = {
            "image": django.forms.FileInput,
        }

    def clean_username(self):
        username = self.cleaned_data[
            apps.users.models.User.username.field.name
        ].lower()
        if username != self.instance.username:
            new = apps.users.models.User.objects.filter(username=username)
            if new.count():
                raise django.core.exceptions.ValidationError(
                    _("Пользователь уже существует"),
                )

        return username

    def clean_email(self):
        email = self.cleaned_data[apps.users.models.User.email.field.name]
        if email != self.instance.email:
            new = apps.users.models.User.objects.filter(email=email)
            if new.count():
                raise django.core.exceptions.ValidationError(
                    _("User with this email already exists"),
                )

        return email

    def clean_password_change_link(self):
        return self.instance.password
