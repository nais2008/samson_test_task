import os
import pathlib

from django.utils.translation import gettext_lazy as _
import dotenv

dotenv.load_dotenv()

__all__ = ()


def get_true_or_false_env(par: str) -> bool:
    parametr = os.environ.get(par, "f").lower()
    return parametr in ("true", "1", "yes", "t", "y", "")


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "yuor_secret_key")

DEBUG = get_true_or_false_env("DJANGO_DEBUG")

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost",
).split(",")

DEFAULT_USER_IS_ACTIVE = get_true_or_false_env("DJANGO_DEFAULT_USER_IS_ACTIVE")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEFAULT_USER_IS_ACTIVE = True

ROOT_URLCONF = "samson.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "samson.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/user/login/"
PASSWORD_RESET_REDIRECT_URL = "/user/login/"
PASSWORD_CHANGE_REDIRECT_URL = "/"
# AUTHENTICATION_BACKENDS = [
#     "apps.users.backends.EmailBackend",
# ]

LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]
STATIC_ROOT = "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
