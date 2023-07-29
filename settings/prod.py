from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

if os.environ.get("SENTRY_ENABLED") == "True":
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN") ,integrations=[DjangoIntegration()] ,traces_sample_rate=1.0 ,send_default_pii=True)