from celery import shared_task
from ticket.models import Ticket
from datetime import timedelta
from django.utils import timezone

@shared_task
def check_old_tickets():
    Ticket.objects.filter(is_active=False, created_at__lt=timezone.now() - timedelta(days=1), ticket_type='REGULAR', transaction_id=None).delete()
    print('Deleted old tickets')