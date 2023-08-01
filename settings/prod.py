from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Email settings if EMAIL_REQUIRED is set to True
if os.environ.get("EMAIL_REQUIRED") == "True":
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "email_host")
    EMAIL_PORT = os.environ.get("EMAIL_PORT", "email_port")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "email_host_user")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "email_host_password")
    EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "email_use_ssl")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

if os.environ.get("SENTRY_ENABLED") == "True":
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN") ,integrations=[DjangoIntegration()] ,traces_sample_rate=1.0 ,send_default_pii=True)