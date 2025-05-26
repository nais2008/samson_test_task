import django.contrib.auth
import django.forms
from django.utils.translation import gettext_lazy as _

import apps.users.models

__all__ = (
    "UserRegistrationForm",
    "UpdateProfileForm",
)

normalizer = apps.users.email_normalizer.EmailNormalizer()


class CustomCheckboxInput(django.forms.CheckboxInput):
    template_name = "widgets/checkbox-input.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["label_text"] = self.attrs.pop("label_text", "")

        if "class" in context["widget"]["attrs"]:
            if "check" not in context["widget"]["attrs"]["class"]:
                context["widget"]["attrs"]["class"] += " check"
        else:
            context["widget"]["attrs"]["class"] = "check"

        return context


class UserCreationForm(
    django.contrib.auth.forms.UserCreationForm,
):
    PERSONAL_DATA_LINK = (
        "https://sakhalinzoo.ru/upload/photos/5ed9c4b3a4680_1591329971.jpg"
    )
    agree_to_data_processing = django.forms.BooleanField(
        required=True,
        label="",
        error_messages={
            "required": _(
                "You must agree to the personal data processing to register.",
            ),
        },
        widget=CustomCheckboxInput(
            attrs={
                "label_text": django.utils.html.format_html(
                    _("Do you agree to provide your <a href='{}'>personal data</a>?"),
                    PERSONAL_DATA_LINK,
                ),
            },
        ),
    )

    def clean_username(self):
        username = self.cleaned_data[apps.users.models.User.username.field.name].lower()
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
        user.email = self.cleaned_data[apps.users.models.User.email.field.name]
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
            "agree_to_data_processing",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["agree_to_data_processing"].label_suffix = ""


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
        username = self.cleaned_data[apps.users.models.User.username.field.name].lower()
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
                    _("Пользователь с таким email уже существует"),
                )

        return email

    def clean_password_change_link(self):
        return self.instance.password
