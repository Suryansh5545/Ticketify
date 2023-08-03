from .common import *

DEBUG = False

# E-Mail Settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
    }
}

CELERY_TASK_ALWAYS_EAGER = True

TEST = True