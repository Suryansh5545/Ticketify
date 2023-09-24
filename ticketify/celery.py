import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.conf.enable_utc = False
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace='CELERY')

# Celery Periodic Tasks
app.conf.beat_schedule = {
    'check-all-transaction-status': {
        'task': 'transactions.tasks.check_all_transaction_status',
        'schedule': 900.0,  # 15 minutes
    },
    'export-all-data': {
        'task': 'base.tasks.export_all_data',
        'schedule': 7200.0,  # 60 minutes
    },
    'check_old_tickets': {
        'task': 'ticket.tasks.check_old_tickets',
        'schedule': 86400.0,  # 1 day
    },
    'check_promo': {
        'task': 'event.tasks.check_promo',
        'schedule': 3600.0,  # 1 hour
    },
    'check_old_transactions': {
        'task': 'transactions.tasks.check_old_transactions',
        'schedule': 86400.0,  # 1 day
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')