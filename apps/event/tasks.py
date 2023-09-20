from celery import shared_task
from event.models import PromoCode
from .utils import send_promo_email

@shared_task
def check_promo():
    promos = PromoCode.objects.filter(email_sended=False, is_active=True, email__isnull=False)
    for promo in promos:
        promo.email_sended = True
        promo.save()
        send_promo_email(promo.pk)
    print('Promo sended')