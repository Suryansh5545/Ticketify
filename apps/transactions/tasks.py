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
                msg = GetMessage().schedule_msg(ticket.order_id)
                url = settings.CONF_BILL_URL
                response = requests.post(url, data={'msg': msg})
                values = ResponseMessage().schedule_resp(response)
                if not values is False and values['MID'] == settings.MID:
                    transaction = Transaction.objects.get(order_id=values['OrderID'])
                    tstat,amnt,txnid,dnt,mode = values['TStat'],values['AMNT'], values['TaxnNo'],values['DnT'],values['TMode']
                    if transaction.payment_id is None and tstat == '0300' and transaction.payment_amount== float(amnt):
                        transaction.payment_id = txnid
                        transaction.payment_amount = amnt
                        transaction.payment_currency = "INR"
                        transaction.payment_method = mode
                        transaction.payment_status = "captured"
                        transaction.save()
                        if ticket.is_active == False:
                            ticket.is_active = True
                            ticket.save()
                            if ticket.ticket_image_generated == False:
                                generate_ticket_image(ticket.pk)
                    elif  tstat == '0300' and transaction.payment_amount== float(amnt):
                        if ticket.is_active == False:
                            ticket.is_active = True
                            ticket.save()
                            if ticket.ticket_image_generated == False:
                                generate_ticket_image(ticket.pk)
                    elif transaction.payment_id is None and tstat == '0300' and transaction.payment_amount!= float(amnt):
                        transaction.payment_id = txnid
                        transaction.payment_amount = amnt
                        transaction.payment_currency = "INR"
                        transaction.payment_method = mode
                        transaction.payment_status = "Mismatch"
                        transaction.save()
                        if ticket.is_active == True:
                            ticket.is_active = False
                            ticket.save()
                    elif transaction.payment_id is None and tstat == '0002':
                        transaction.payment_status = "Pending"
                        transaction.save()
                        if ticket.is_active == True:
                            ticket.is_active = False
                            ticket.save()
                    elif tstat != '0300':
                        ticket.is_active = False
                        ticket.save()
                        if tstat == '0399':
                            transaction.payment_status = "Failed"
                            transaction.payment_method = mode
                            transaction.save()
                        elif tstat == "NA":
                            transaction.payment_status = "Cancel"
                            transaction.payment_method = mode
                            transaction.save()
                        elif tstat == "0001":
                            transaction.payment_status = "Cancel"
                            transaction.payment_method = mode
                            transaction.save()
                        else:
                            transaction.payment_status = "Failed"
                            transaction.payment_method = mode
                            transaction.save()
                    else:
                        transaction.payment_status = "Failed"
                        transaction.payment_method = mode
                        transaction.save()
        else:
            if ticket.ticket_image_generated == False:
                generate_ticket_image(ticket.pk)
                ticket.ticket_image_generated = True
                ticket.save()
    print("All Transactions Checked")
