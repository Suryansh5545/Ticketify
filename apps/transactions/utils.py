from event.models import Event, SubEvent, Addon, PromoCode
import os, razorpay, json
from ticket.models import Ticket
from transactions.models import Transaction
from ticket.utils import create_ticket, generate_ticket_image
from base.utils import get_url_from_hostname
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


def HandlePriceCalculation(request):
    event_id = request.data.get('event_id')
    selected_sub_events = request.data.get('selected_sub_events', []),
    selected_addons = request.data.get('selected_addons', [])
    couponcode = request.data.get('coupon', '')
    total_sub_event_allowed = Event.objects.get(pk=event_id).sub_events_included_allowed
    sub_event_count = 0
    sub_event_price = 0
    addon_price = 0
    for sub_event in selected_sub_events[0]:
        if sub_event_count < total_sub_event_allowed:
            sub_event_count += 1
        else:
            sub_event_price += SubEvent.objects.get(pk=sub_event).price
    for addon in selected_addons:
        addon_price += Addon.objects.get(pk=addon).price
    event_price = Event.objects.get(pk=event_id).price
    total_price = event_price + sub_event_price + addon_price
    if couponcode != '':
        try:
            promocode = PromoCode.objects.get(code=couponcode)
        except promocode.DoesNotExist:
            promocode = None
        if promocode:
            if (total_price- promocode.discount) < 0:
                    total_price = total_price - promocode.discount
    return int(total_price)


def payment_gateway(request):
    Total_amount = HandlePriceCalculation(request)
    data = {
        "amount": Total_amount * 100,
        "currency": "INR",
        "notes": {
            "name": request.data.get('customer_name'),
            "email": request.data.get('customer_email'),
            "phone": request.data.get('customer_phone'),
            "referral": request.data.get('referral'),
            "event_id": request.data.get('event_id'),
            "selected_sub_events": json.dumps(request.data.get('selected_sub_events')),
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
            create_ticket(request, order['id'])
            payment_info = {"message": "Order Created", 
                            "payment_id": order['id'],
                            "amount": order['amount'],
                            "currency": order['currency'], 
                            "id": settings.RAZORPAY_KEY,
                            "Business": "JKLU",
                            "callback_url": get_url_from_hostname(settings.HOSTNAME) + "/api/transactions/handle-payment-success/",
                            "image": "https://sabrang.jklu.edu.in/wp-content/uploads/2022/10/sabrang-cover-text-e1664621537950.png"}
            
            return payment_info
        

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