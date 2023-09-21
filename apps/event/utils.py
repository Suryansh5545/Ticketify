from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from event.models import PromoCode



@shared_task(name="send_promo_email")
def send_promo_email(promo_pk):
    promo = PromoCode.objects.get(pk=promo_pk)
    recipient_email = promo.email
    recipient_name = promo.name
    event_name = promo.event.name
    email_data = {
        "recipient_name": recipient_name,
        "promo_code": promo.code,
    }
    html_content = render_to_string('email/promo_template.html', email_data)
    email = EmailMultiAlternatives(f"UNIQUE CODE FOR {event_name} REGISTRATION", "Please find your unique code attached", settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach_alternative(html_content, "text/html")
    # Send the email
    email.send()