import os

from config.settings.base import *  # noqa: F403, F401

DEBUG = False
ALLOWED_HOSTS = ["mydomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # noqa: F405
STATICFILES_DIRS = []
