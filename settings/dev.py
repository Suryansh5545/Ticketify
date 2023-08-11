from .common import *

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
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

SFTP_STORAGE_HOST = getenv("SFTP_STORAGE_HOST", "sftp_storage_host")
SFTP_STORAGE_ROOT = getenv("SFTP_STORAGE_ROOT", "sftp_storage_root")
SFTP_STORAGE_PARAMS = {
    'port': getenv("SFTP_STORAGE_PORT", "sftp_storage_port"),
    'username': getenv("SFTP_STORAGE_USERNAME", "sftp_storage_username"),
    'password': getenv("SFTP_STORAGE_PASSWORD", "sftp_storage_password"),
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
