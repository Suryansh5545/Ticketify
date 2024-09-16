from event.models import Event, SubEvent, Addon, PromoCode
import os, razorpay, json
from ticket.models import Ticket
from transactions.models import Transaction
from ticket.utils import create_ticket, generate_ticket_image
from base.utils import get_url_from_hostname
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django_billdesk import ResponseMessage, GetMessage

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


def HandlePriceCalculation(request):
    promo_applied = False
    event_id = request.data.get('event_id')
    selected_sub_events = request.data.get('selected_sub_events', []),
    selected_addons = request.data.get('selected_addons', [])
    couponcode = request.data.get('coupon', '')
    total_sub_event_allowed = Event.objects.get(pk=event_id).sub_events_included_allowed
    flagship_event_included_allowed = Event.objects.get(pk=event_id).flagship_event_included_allowed
    flagship_sub_event_count = 0
    sub_event_count = 0
    sub_event_price = 0
    addon_price = 0
    # Check for premium sub events
    for sub_event in selected_sub_events[0]:
        if SubEvent.objects.get(pk=sub_event['id']).type == 'premium':
            if flagship_sub_event_count < flagship_event_included_allowed and sub_event['given']:
                flagship_sub_event_count += 1
            else:
                sub_event_price += SubEvent.objects.get(pk=sub_event['id']).price
    for sub_event in selected_sub_events[0]:
        if SubEvent.objects.get(pk=sub_event['id']).type == 'standard':
            if sub_event_count < total_sub_event_allowed and sub_event['given']:
                sub_event_count += 1
            else:
                if SubEvent.objects.get(pk=sub_event['id']):
                    sub_event_price += SubEvent.objects.get(pk=sub_event['id']).price
    for addon in selected_addons:
        addon_price += Addon.objects.get(pk=addon).price
        Addon.objects.get(pk=addon).stock -= 1
        Addon.objects.get(pk=addon).save()
    if request.data.get('customer_type') == 'SCHOOL':
        event_price = Event.objects.get(pk=event_id).student_price
    else:
        event_price = Event.objects.get(pk=event_id).price
    total_price = event_price + sub_event_price + addon_price
    if couponcode != '':
        try:
            promocode = PromoCode.objects.get(code__iexact=couponcode)
        except promocode.DoesNotExist:
            promocode = None
        if promocode and promocode.stock > 0 and (request.data.get('customer_type') != 'SCHOOL'):
            if not ((total_price- promocode.discount) <= 0):
                    total_price = total_price - promocode.discount
                    promo_applied = True
    return int(total_price), promo_applied


def payment_gateway(request):
    Total_amount, promo_applied = HandlePriceCalculation(request)
    selected_sub_events = request.data.get('selected_sub_events')
    if selected_sub_events:
        first_id = selected_sub_events[0].get('id')
        selected_sub_events = json.dumps(first_id)
    else:
        selected_sub_events = None
    data = {
        "amount": Total_amount * 100,
        "currency": "INR",
        "notes": {
            "name": request.data.get('customer_name'),
            "email": request.data.get('customer_email'),
            "phone": request.data.get('customer_phone'),
            "referral": request.data.get('referral'),
            "event_id": request.data.get('event_id'),
            "selected_sub_events": selected_sub_events,
            "selected_addons": json.dumps(request.data.get('selected_addons'))
        }
    }

    event = Event.objects.get(pk=request.data.get('event_id'))
    if event.payment_gateway == "razorpay":
        order = client.order.create(data=data)
        if "error" in order:
            return Response({"message": "Backend Error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Transaction.objects.create(payment_status="created", 
                                    order_id=order['id'], 
                                    payment_amount=order['amount']/100, 
                                    payment_currency=order['currency'])
            create_ticket(request, order['id'], promo_applied)
            payment_info = {"message": "Order Created", 
                            "payment_id": order['id'],
                            "amount": order['amount'],
                            "currency": order['currency'], 
                            "id": settings.RAZORPAY_KEY,
                            "Business": "JKLU",
                            "callback_url": get_url_from_hostname(settings.HOSTNAME) + "/api/transactions/handle-payment-success/",
                            "image": "https://sabrang.jklu.edu.in/wp-content/uploads/2022/10/sabrang-cover-text-e1664621537950.png"}
            return payment_info
            
    if event.payment_gateway == "billdesk":
            ticket = create_ticket(request, None, promo_applied)
            Transaction.objects.create(payment_status="created", 
                                       order_id=ticket.id, 
                                        payment_amount=Total_amount,
                                        payment_currency="INR")
            ticket.order_id = ticket.id
            ticket.save()
            msg = GetMessage().message(ticket.id, Total_amount, request.data.get('customer_email'), request.data.get('customer_phone'), request.data.get('customer_name'), ticket.check_in)
            return msg
        

def verify_payment_razorpay(request):
    razorpay_payment_id = request.data.get('razorpay_payment_id')
    razorpay_order_id = request.data.get('razorpay_order_id')
    razorpay_signature = request.data.get('razorpay_signature')
    if razorpay_payment_id == None or razorpay_order_id == None or razorpay_signature == None:
            error_reason = request.data.get('error[reason]')
            html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: {error_reason}</p></body></html>"
            return html_response
    params_dict = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_signature': razorpay_signature
    }
    payment_complete = client.utility.verify_payment_signature(params_dict)
    if payment_complete:
        transaction = Transaction.objects.get(order_id=razorpay_order_id)
        transaction.payment_id = razorpay_payment_id
        payment_details = client.payment.fetch(transaction.payment_id)
        transaction.payment_status = payment_details['status']
        transaction.payment_method = payment_details['method']
        transaction.save()
        return transaction
    else:
        html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: Signature Verification Failed</p></body></html>"
        return html_response
    

def verify_payment_billdesk(values):
    if not values is False and values['MID'] == settings.MID:
        transaction = Transaction.objects.get(order_id=values['OrderID'])
        tstat,amnt,txnid,dnt,mode = values['TStat'],values['AMNT'], values['TaxnNo'],values['DnT'],values['TMode']
        transaction.payment_id = txnid
        Ticket.objects.filter(order_id=values['OrderID']).update(transaction_id=transaction)
        if tstat == '0300' and transaction.payment_amount== float(amnt):
            transaction.payment_status = "captured"
            transaction.payment_method = mode
            transaction.save()
            return transaction
        elif tstat == '0300' and transaction.payment_amount!= float(amnt):
            transaction.payment_status = "Mismatch"
            transaction.payment_method = mode
            transaction.save()
            html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: Amount Mismatch</p></body></html>"
            return html_response
        elif tstat == '0002':
            transaction.payment_status = "Pending"
            transaction.payment_method = mode
            transaction.save()
            html_response = f"<html><body><h1>Payment Failed</h1><p>Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response</p></body></html>"
            return html_response
        elif tstat != '0300':
            if tstat == '0399':
                transaction.payment_status = "Failed"
                transaction.payment_method = mode
                transaction.save()
                html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: Invalid Authentication at Bank</p></body></html>"
            elif tstat == "NA":
                transaction.payment_status = "Cancel"
                transaction.payment_method = mode
                transaction.save()
                html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: Invalid Input in the Request Message</p></body></html>"
            elif tstat == "0001":
                transaction.payment_status = "Cancel"
                transaction.payment_method = mode
                transaction.save()
                html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: error at billdesk</p></body></html>"
            else:
                transaction.payment_status = "Failed"
                transaction.payment_method = mode
                transaction.save()
                html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed.</p></body></html>"
            return html_response
        else:
            transaction.payment_status = "Failed"
            transaction.payment_method = mode
            transaction.save()
            html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed.</p></body></html>"
            return html_response
    else:
        html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: Looked liked someone tried tampering your payment</p></body></html>"
        return html_response
