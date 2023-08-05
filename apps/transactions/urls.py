from django.urls import path
from .views import HandlePayment, HandlePaymentSuccess, PaymentWebhook

urlpatterns = [
    path("handle-payment/", HandlePayment.as_view(), name="handle_payment"),
    path("handle-payment-success/", HandlePaymentSuccess.as_view(), name="handle_payment_success"),
    path("payment-webhook/", PaymentWebhook.as_view(), name="payment_webhook"),
]