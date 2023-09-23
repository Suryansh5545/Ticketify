from celery import shared_task
from ticket.models import Ticket
from datetime import timedelta
from django.utils import timezone

@shared_task
def check_old_tickets():
    tickets = Ticket.objects.filter(is_active=False, created_at__lt=timezone.now() - timedelta(hours=1), ticket_type='REGULAR', transaction_id=None)
    for ticket in tickets:
        if ticket.promo_applied == True:
            promo = ticket.promocode
            if promo is not None:
                promo.stock += 1
                promo.save()
        ticket.delete()
    print('Deleted old tickets')