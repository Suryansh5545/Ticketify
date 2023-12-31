from base.utils import get_url_from_hostname
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Transaction
from ticket.utils import create_ticket, generate_ticket_image
from ticket.models import Ticket
from event.models import Event
from django.http import HttpResponse
import os, razorpay, json
from base.utils import EmailService
from .utils import payment_gateway, verify_payment_razorpay


client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

class HandlePayment(APIView):
    """
    Handle Payment
    """
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
                return_data = payment_gateway(request)
                return Response(return_data, status=status.HTTP_200_OK)


class HandlePaymentSuccess(APIView):
    """
    Handle Payment Success
    """
    def post(self, request):
        event = Event.objects.get(is_active=True)
        if event.payment_gateway == "razorpay":
            transaction = verify_payment_razorpay(request)
        if isinstance(transaction, Transaction):
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
                try:
                    task_id = ticket_url.id
                except TimeoutError:
                    html_response = "<html><body><h1>Ticket Generation Pending</h1><p>Payment Done , Your Ticket will be mailed to your email.</p></body></html>"
                    return HttpResponse(html_response, status=400)

                if task_id:
                    return redirect(get_url_from_hostname(settings.FRONTEND_URL) + "/delivery/" + task_id)
                else:
                    html_response = "<html><body><h1>Invalid Payment</h1><p>This Payment ID doesn't match our database, if you believe this is a error contact us at our support mail at our homepage.</p></body></html>"
                    return HttpResponse(html_response, status=400)
            else:
                html_response = "<html><body><h1>Invalid Payment</h1><p>The Payment failed, if you believe this is a error contact us at our support mail at our homepage.</p></body></html>"
                return HttpResponse(html_response, status=400)
        else:
            return Response({"message": transaction}, status=status.HTTP_400_BAD_REQUEST)
            

class PaymentWebhook(APIView):
    """
    Handle Payment Webhook
    """
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