from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False

# Admin settings
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "example@example.com")

# Email settings if EMAIL_REQUIRED is set to True
if os.environ.get("EMAIL_REQUIRED") == "True":
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "email_host")
    EMAIL_PORT = os.environ.get("EMAIL_PORT", "email_port")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "email_host_user")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "email_host_password")
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "email_use_tls")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME", "ticketify"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

CORS_ALLOWED_ORIGINS = [
    "https://ticketify.tech",
    "https://sabrang.ticketify.tech",
    "https://staging.ticketify.tech",
    "https://ticketify.hackjklu.com",
]

# S3 Bucket settings
AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME", "aws_storage_bucket_name")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID", "aws_access_key_id")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY", "aws_secret_access_key")
AWS_S3_ENDPOINT_URL = getenv("AWS_S3_ENDPOINT_URL", "aws_s3_endpoint_url")
AWS_DEFAULT_ACL = 'public-read'

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage" },
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}
}

SFTP_STORAGE_HOST = getenv("SFTP_STORAGE_HOST", "sftp_storage_host")
SFTP_STORAGE_ROOT = getenv("SFTP_STORAGE_ROOT", "sftp_storage_root")
SFTP_STORAGE_PARAMS = {
    'port': getenv("SFTP_STORAGE_PORT", "sftp_storage_port"),
    'username': getenv("SFTP_STORAGE_USERNAME", "sftp_storage_username"),
    'password': getenv("SFTP_STORAGE_PASSWORD", "sftp_storage_password"),
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if os.environ.get("SENTRY_ENABLED") == "True":
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN") ,integrations=[DjangoIntegration()] ,traces_sample_rate=1.0 ,send_default_pii=True)