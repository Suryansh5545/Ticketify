from base.utils import get_url_from_hostname
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Transaction
from ticket.utils import create_ticket, generate_ticket_image
from ticket.models import Ticket
from event.models import Event, SubEvent, Addon
from django.http import HttpResponse
import os, razorpay, json
from base.utils import EmailService


client = razorpay.Client(auth=(os.environ.get("RAZORPAY_KEY"), os.environ.get("RAZORPAY_SECRET")))

class HandlePayment(APIView):
    def post(self, request):
        if (os.environ.get("PAYMENT_ENV") == "development"):
            transaction = Transaction.objects.create(payment_method="card", payment_status="success", payment_id="1234567890", payment_amount=1000, payment_currency="NGN")
            if transaction.payment_status == "success":
                ticket_status = create_ticket(request, "1234567890")
                if ticket_status == True:
                    return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Total_amount = HandlePriceCalculation(request)
            data = {
                "amount": Total_amount * 100,
                "currency": "INR",
                "notes": {
                    "name": request.data.get('customer_name'),
                    "email": request.data.get('customer_email'),
                    "phone": request.data.get('customer_phone'),
                    "event_id": request.data.get('event_id'),
                    "selected_sub_events": json.dumps(request.data.get('selected_sub_events')),
                    "selected_addons": json.dumps(request.data.get('selected_addons'))
                }
            }
            order = client.order.create(data=data)
            if "error" in order:
                return Response({"message": "Backend Error"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Transaction.objects.create(payment_status="created", 
                                        order_id=order['id'], 
                                        payment_amount=order['amount']/100, 
                                        payment_currency=order['currency'])
                create_ticket(request, order['id'])
                return_data = {"message": "Order Created", 
                                "payment_id": order['id'],
                                "amount": order['amount'],
                                "currency": order['currency'], 
                                "id": (os.environ.get("RAZORPAY_KEY")),
                                "Business": "JKLU",
                                "callback_url": get_url_from_hostname(settings.HOSTNAME) + "/api/transactions/handle-payment-success/",
                                "image": "https://sabrang.jklu.edu.in/wp-content/uploads/2022/10/sabrang-cover-text-e1664621537950.png"}
                return Response(return_data, status=status.HTTP_200_OK)


def HandlePriceCalculation(request):
    event_id = request.data.get('event_id')
    selected_sub_events = request.data.get('selected_sub_events', []),
    selected_addons = request.data.get('selected_addons', [])
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
    return int(total_price)


class HandlePaymentSuccess(APIView):
    def post(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        if razorpay_payment_id == None or razorpay_order_id == None or razorpay_signature == None:
                error_reason = request.data.get('error[reason]')
                html_response = f"<html><body><h1>Payment Failed</h1><p>Sorry, your payment has failed. Reason: {error_reason}</p></body></html>"
                return HttpResponse(html_response, status=400)
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
        if transaction.payment_status == "captured":
            ticket = Ticket.objects.get(order_id = transaction.order_id)
            ticket.transaction_id = transaction
            ticket.is_active = True
            if ticket.ticket_image_generated == False:
                ticket_url = generate_ticket_image.delay(ticket.id)
                ticket.ticket_image_generated = True
            else:
                html_response = "<html><body><h1>Payment Already Done</h1><p>This Payment is already Handled and ticket mailed.</p></body></html>"
                return HttpResponse(html_response, status=400)
            ticket.save()
            # Wait for the Celery task to complete using the get() method with a timeout
            try:
                ticket_url = ticket_url.get(timeout=60)  # Adjust the timeout value as needed
            except TimeoutError:
                html_response = "<html><body><h1>Ticket Generation Pending</h1><p>Payment Done , Your Ticket will be mailed to your email.</p></body></html>"
                return HttpResponse(html_response, status=400)

            if ticket_url:
                return redirect(ticket_url)
            else:
                html_response = "<html><body><h1>Invalid Payment</h1><p>This Payment ID doesn't match our database, if you believe this is a error contact us at our support mail at our homepage.</p></body></html>"
                return HttpResponse(html_response, status=400)
        else:
            html_response = "<html><body><h1>Invalid Payment</h1><p>The Payment failed, if you believe this is a error contact us at our support mail at our homepage.</p></body></html>"
            return HttpResponse(html_response, status=400)
            

class PaymentWebhook(APIView):
    def post(self, request):
        payload_body = json.dumps(request.data, separators=(',', ':'))
        webhook_signature = request.headers.get("X-Razorpay-Signature")
        webhook_secret = os.environ.get("RAZORPAY_WEBHOOK_SECRET")
        webhook_valid = client.utility.verify_webhook_signature(payload_body, webhook_signature, webhook_secret)
        if webhook_valid:
            data = json.loads(payload_body)
            if data['event'] == "order.paid":
                transaction = Transaction.objects.get(order_id=data['payload']['order']['entity']['id'])
                transaction.payment_status = "captured"
                transaction.webhook_recieved = True
                if transaction.payment_id == "":
                    transaction.payment_id = data['payload']['payment']['entity']['id']
                transaction.payment_method = data['payload']['payment']['entity']['method']
                transaction.save()
                ticket = Ticket.objects.get(order_id = transaction.order_id)
                ticket.transaction_id = transaction
                ticket.is_active = True
                if ticket.ticket_image_generated == False:
                    image = generate_ticket_image(ticket.id)
                    ticket.ticket_image_generated = True
                else:
                    return Response({"message": "Webhook recieved"}, status=status.HTTP_200_OK)
                ticket.save()
                return Response({"message": "Order Paid Notified"}, status=status.HTTP_202_ACCEPTED)
            elif data['event'] == "payment.captured":
                transaction = Transaction.objects.get(order_id=data['payload']['payment']['entity']['order_id'])
                if transaction.webhook_recieved == True:
                    return Response({"message": "Webhook Confirmation already Recieved"}, status=status.HTTP_200_OK)
                transaction.payment_status = "captured"
                if transaction.payment_id == "":
                    transaction.payment_id = data['payload']['payment']['entity']['id']
                transaction.webhook_recieved = True
                transaction.payment_method = data['payload']['payment']['entity']['method']
                transaction.save()
                ticket = Ticket.objects.get(order_id = transaction.order_id)
                ticket.transaction_id = transaction
                ticket.is_active = True
                if ticket.ticket_image_generated == False:
                    image = generate_ticket_image(ticket.id)
                    ticket.ticket_image_generated = True
                else:
                    return Response({"message": "Webhook recieved"}, status=status.HTTP_200_OK)
                ticket.save()
                return Response({"message": "Payment Captured Notified"}, status=status.HTTP_200_OK)
            elif data['event'] == "payment.failed":
                transaction = Transaction.objects.get(order_id=data['payload']['payment']['entity']['order_id'])
                transaction.payment_status = "failed"
                transaction.webhook_recieved = True
                transaction.save()
                ticket = Ticket.objects.get(order_id = transaction.order_id)
                ticket.transaction_id = transaction
                ticket.is_active = False
                ticket.save()
                return Response({"message": "Payment Captured Notified"}, status=status.HTTP_202_ACCEPTED)
            elif data['event'] == "payment.dispute.created":
                transaction = Transaction.objects.get(order_id=data['payload']['payment']['entity']['order_id'], payment_id=data['payload']['payment']['entity']['id'])
                transaction.payment_status = "disputed"
                transaction.save()
                ticket = Ticket.objects.get(order_id = transaction.order_id)
                ticket.is_active = False
                ticket.save()
                message = "Dispute Created for Order ID: " + data['payload']['payment']['entity']['order_id'] + " Payment ID: " + data['payload']['payment']['entity']['id'] + " Amount: " + data['payload']['payment']['entity']['amount'] + " Reason: " + data['payload']['dispute']['entity']['reason_code']
                EmailService.send_email("Payment Disputed", message, os.environ.get("NOTIFICATION_EMAIL"))
                return Response({"message": "Payment Disputed Notified"}, status=status.HTTP_202_ACCEPTED)
            elif data['event'] == "refund.created":
                transaction = Transaction.objects.get(order_id=data['payload']['payment']['entity']['order_id'], payment_id=data['payload']['payment']['entity']['id'])
                transaction.payment_status = "refunded"
                transaction.save()
                ticket = Ticket.objects.get(order_id = transaction.order_id)
                ticket.is_active = False
                ticket.save()
                return Response({"message": "Payment Refunded Notified"}, status=status.HTTP_202_ACCEPTED)
            else:
                message = "Webhook recieved for " + data['event'] + "Unable to handle this event"
                EmailService.send_email("Unknown Webhook Recieved", message, os.environ.get("NOTIFICATION_EMAIL"))
                return Response({"message": "Webhook recieved"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid Webhook Signature"}, status=status.HTTP_400_BAD_REQUEST)