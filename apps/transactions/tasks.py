import razorpay
from celery import shared_task
from .models import Transaction
from ticket.models import Ticket
from django.conf import settings
from ticket.utils import generate_ticket_image

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

@shared_task
def check_all_transaction_status():
    tickets = Ticket.objects.all()
    for ticket in tickets:
        if ticket.ticket_type == "REGULAR":
            order = client.order.fetch(ticket.order_id)
            if order["status"] == "paid":
                payment = client.order.payments(ticket.order_id)
                payment_status = payment["items"][0]["status"]
                if payment_status != ticket.transaction_id.payment_status:
                    ticket.transaction_id.payment_status = payment_status
                    ticket.save()
                if ticket.is_active == False and ticket.transaction_id.payment_status == "captured":
                    ticket.is_active = True
                    if ticket.ticket_image_generated == False:
                        generate_ticket_image(ticket.pk)
                    ticket.save()
                elif ticket.is_active == True and ticket.transaction_id.payment_status != "captured":
                    ticket.is_active = False
                    ticket.save()
            else:
                ticket.save()
                if ticket.is_active == True:
                    ticket.is_active = False
                    ticket.save()
        else:
            if ticket.ticket_image_generated == False:
                generate_ticket_image(ticket.pk)
                ticket.ticket_image_generated = True
                ticket.save()
