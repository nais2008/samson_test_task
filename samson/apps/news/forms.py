import django.forms

import apps.news.models

__all__ = ["NewsForm"]


class NewsForm(django.forms.ModelForm):
    image = django.forms.ImageField(
        required=False,
        label="Image",
        help_text="Upload an image for the news",
    )

    class Meta:
        model = apps.news.models.News
        exclude = [
            apps.news.models.News.id.field.name,
            apps.news.models.News.data.field.name,
            apps.news.models.News.user.field.name,
        ]

    def save(self, commit=True, user=None):
        news_instance = super().save(commit=False)

        if user is not None:
            news_instance.user = user

        if commit:
            news_instance.save()

            image_file = self.cleaned_data.get("image")
            if image_file:
                apps.news.models.Image.objects.update_or_create(
                    news=news_instance,
                    defaults={'image': image_file}
                )
            elif 'image' in self.changed_data and not image_file:
                apps.news.models.Image.objects.filter(news=news_instance).delete()

        return news_instance


class UpdateNewsForm(django.forms.ModelForm):
    class Meta:
        model = apps.news.models.News
        exclude = [
            apps.news.models.News.id.field.name,
            apps.news.models.News.data.field.name,
            apps.news.models.News.user.field.name,
        ]


class NewsImageForm(django.forms.ModelForm):
    class Meta:
        model = apps.news.models.Image
        fields = [
            apps.news.models.Image.image.field.name,
        ]
        exclude = [
            apps.news.models.Image.news.field.name,
        ]
