import razorpay
from celery import shared_task
from .models import Transaction
from ticket.models import Ticket
from django.conf import settings
from ticket.utils import generate_ticket_image

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

@shared_task
def check_all_transaction_status():
    transactions = Transaction.objects.all
    for transaction in transactions:
        payment = client.payment.fetch(transaction.order_id)
        if payment["status"] != transaction.payment_status:
            transaction.payment_status = payment["status"]
            transaction.save()
        ticket = Ticket.objects.get(transaction_id=transaction)
        if ticket.is_active == False and transaction.payment_status == "captured":
            ticket.is_active = True
            if ticket.ticket_image_generated == False:
                generate_ticket_image(ticket)
            ticket.save()
        elif ticket.is_active == True and transaction.payment_status != "captured":
            ticket.is_active = False
            ticket.save()

