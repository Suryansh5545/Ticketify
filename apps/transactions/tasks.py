import razorpay
from celery import shared_task
from .models import Transaction
from ticket.models import Ticket
from django.conf import settings
from ticket.utils import generate_ticket_image

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

@shared_task
def check_all_transaction_status():
    transactions = Transaction.objects.all()
    for transaction in transactions:
        try:
            ticket = Ticket.objects.get(transaction_id=transaction)
        except Ticket.DoesNotExist:
            ticket = None
        if ticket:
            order = client.order.fetch(transaction.order_id)
            if order["status"] == "paid":
                payment = client.order.payments(transaction.order_id)
                payment_status = payment["items"][0]["status"]
                if payment_status != transaction.payment_status:
                    transaction.payment_status = payment_status
                    transaction.save()
                if ticket.is_active == False and transaction.payment_status == "captured":
                    ticket.is_active = True
                    if ticket.ticket_image_generated == False:
                        generate_ticket_image(ticket)
                    ticket.save()
                elif ticket.is_active == True and transaction.payment_status != "captured":
                    ticket.is_active = False
                    ticket.save()
            else:
                transaction.payment_status = order["status"]
                transaction.save()
                ticket = Ticket.objects.get(transaction_id=transaction)
                if ticket.is_active == True:
                    ticket.is_active = False
                    ticket.save()
        else:
            print("Ticket not found for transaction id: ", transaction.id)
