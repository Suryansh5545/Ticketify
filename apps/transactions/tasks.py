from django.utils import timezone
from datetime import timedelta
import razorpay
from celery import shared_task
from .models import Transaction
from ticket.models import Ticket
from django.conf import settings
from ticket.utils import generate_ticket_image
from event.models import Event
from django_billdesk import GetMessage, ResponseMessage
import requests

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

@shared_task
def check_all_transaction_status():
    try:
        tickets = Ticket.objects.all()
        event = Event.objects.get(is_active=True)
        for ticket in tickets:
            if ticket.ticket_type == "REGULAR":
                if event.payment_gateway == "razorpay":
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
                elif event.payment_gateway == "billdesk":
                    if ticket.is_active == False:
                        msg = GetMessage().schedule_msg(ticket.order_id)
                        url = settings.CONF_BILL_URL
                        response = requests.post(url, data={'msg': msg})
                        values = ResponseMessage().schedule_resp(response)
                        tstat,txnid = values['TStat'], values['TaxnNo']
                        if tstat == "0300":
                            transaction = Transaction.objects.get(order_id=values['OrderID'])
                            if (transaction.payment_status != "Abuse"):
                                transaction.payment_id = txnid
                                transaction.payment_status = "captured"
                                transaction.payment_method = "Unknown"
                                transaction.save()
                                ticket.transaction_id = transaction
                                ticket.is_active = True
                                ticket.save()
                                if ticket.promo_applied == True and ticket.promocode:
                                    ticket.promocode.stock -= 1
                                    ticket.promocode.save()
                                if ticket.ticket_image_generated == False:
                                    if ticket.customer_type == "STUDENT":
                                        if ticket.id_verified == True:
                                            generate_ticket_image.delay(ticket.id)
                                    else:
                                        generate_ticket_image.delay(ticket.id)
            elif ticket.ticket_type == "STUDENT":
                if ticket.ticket_image_generated == False:
                    generate_ticket_image(ticket.pk)
                    ticket.ticket_image_generated = True
                    ticket.save()
        print("All Transactions Checked")
    except Ticket.DoesNotExist:
        print("No Ticket Exist Task")


@shared_task
def check_old_transactions():
    Transaction.objects.filter(payment_status="created", created_at__lt=timezone.now() - timedelta(days=6)).delete()
    print('Deleted old transactions')
