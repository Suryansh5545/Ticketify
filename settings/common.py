"""
Django settings for ticketify project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from os import getenv
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = os.path.join(BASE_DIR, "apps")

sys.path.append(APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "random_secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEST = False

ALLOWED_HOSTS = [getenv("ALLOWED_HOSTS", "*")]


# Application definition


DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OUR_APPS = [
    'base',
    'event',
    'ticket',
    'transactions',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'import_export',
    'dj_rest_auth',
    'storages',
    'drf_yasg'
]

INSTALLED_APPS = DEFAULT_APPS + OUR_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ticketify.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
   'rest_framework.permissions.AllowAny',
   ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/minute",
        "user": "150/minute",
    },
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'ticketify-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'ticketify-refresh-token',
}

WSGI_APPLICATION = 'ticketify.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

TICKETIFY_API_SERVER = os.environ.get(
    "TICKETIFY_API_SERVER", "http://localhost:8000"
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL" , "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND" , "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_HOST_URL", "redis://localhost:6379"),
        'OPTIONS': {
            "db": "10",
        }
    }
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [getenv("CORS_ALLOWED_ORIGINS", "http://localhost:4200")]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

if getenv("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = getenv("CSRF_TRUSTED_ORIGINS").split(",")
else:
    CSRF_TRUSTED_ORIGINS = []

HOSTNAME = os.environ.get("HOSTNAME", "localhost:8000")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "localhost:4200")

# Razorpay settings
RAZORPAY_KEY = os.environ.get("RAZORPAY_KEY", "")
RAZORPAY_SECRET = os.environ.get("RAZORPAY_SECRET", "")

# BillDesk settings
MID = os.environ.get("BILLDESK_MID", "")
SEC_ID = os.environ.get("BILLDESK_SECRET", "")
BILL_URL = os.environ.get("BILL_URL", "")
CONF_BILL_URL = os.environ.get("CONF_BILL_URL", "")
CHECKSUM_KEY = os.environ.get("CHECKSUM_KEY", "")
REVERSE_URL = os.environ.get("REVERSE_URL", "")