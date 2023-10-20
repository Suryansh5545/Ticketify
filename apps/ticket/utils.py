import io
from cryptography.fernet import Fernet
from celery import shared_task
from django.template.loader import get_template
import base64
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
import os, qrcode, imgkit
from io import BytesIO
from .serializers import TicketSerializer
from .models import Ticket, TicketEmailLog
from event.models import Event, PromoCode
from django.conf import settings
from django.core.files import File
from django.template.loader import render_to_string
from django.core.files.base import ContentFile


def create_ticket(request, order_id=None, promo_applied=False):
        if request.method == "POST":
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                customer_name = validated_data['customer_name']
                customer_email = validated_data['customer_email']
                customer_phone = validated_data['customer_phone']
                customer_type = validated_data['customer_type']
                college_name = validated_data.get('college_name', None)
                verification_id = validated_data.get('verification_id', None)
                referral = validated_data.get('referral', None)
                event_id = validated_data['event_id']
                selected_sub_events = validated_data.get('selected_sub_events', [])
                selected_sub_events = [sub_event['id'] for sub_event in selected_sub_events]
                selected_addons = validated_data.get('selected_addons', [])
                promo_code = validated_data.get('coupon', None)
                event = Event.objects.get(pk=event_id)
                ticket = Ticket.objects.create(
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    customer_type=customer_type,
                    college_name=college_name,
                    referral=referral,
                    event=event,order_id = order_id,
                    promo_applied=promo_applied
                )
                if promo_applied:
                    promo = PromoCode.objects.get(code__iexact=promo_code)
                    ticket.promocode = promo
                if verification_id:
                    image_data = base64.b64decode(verification_id)
                    image_name = f"verification_{customer_name}.jpg"
                    image_file = ContentFile(image_data, name=image_name)
                    ticket.verification_id.save(image_file.name, image_file, save=True)
                ticket.selected_sub_events.set(selected_sub_events)
                ticket.selected_addons.set(selected_addons)
                ticket.save()
            else:
                raise Exception(serializer.errors)
        return ticket


@shared_task(name="generate_ticket_image")
def generate_ticket_image (ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    encrypted_ticket_id = encrypt_decrypt_ticket_id(ticket.id)
    qr_code_image = generate_qr_code(ticket.check_in)
    qr_code_image_base64 = base64.b64encode(qr_code_image).decode('utf-8')
    sub_events = ticket.selected_sub_events.all().values_list('name', flat=True)
    if ticket.promo_applied:
        student = "JKLU"
    elif ticket.customer_type == "SCHOOL":
        student = "School"
    else:
        student = ""
    ticket_data = {
            "spam": "",
            "ticketNumber": ticket.id,
            "artistName": ticket.customer_name,
            "showName": ticket.event.name,
            "location": ticket.event.location,
            "day": ticket.event.start_date.strftime("%A"),
            "date": ticket.event.start_date.strftime("%d %B %Y") + " - " + ticket.event.end_date.strftime("%d %B %Y"),
            "year": ticket.event.start_date.strftime("%Y"),
            "timeSlot": ticket.event.start_date.strftime("%I:%M %p"),
            "doors": sub_events,
            "barcodeImageURL": f"data:image/png;base64,{qr_code_image_base64}",
            "ticketType": student,
        }

    template = get_template('ticket/sabrang/index.html')
    html_content = template.render(ticket_data)
    options = {
        'quality': 100,
        'crop-w': '300',
        'crop-y': '40',
        'crop-x': '305',
        'crop-h': '600',
        'zoom': '2',
    }
    ticket_name = f"ticket_{encrypted_ticket_id}.jpg"
    img_bytes = imgkit.from_string(html_content, None, options=options)
    img_io = io.BytesIO(img_bytes)
    ticket.ticket_image.save(ticket_name, File(img_io), save=True)
    ticket.ticket_image_generated = True
    ticket.save()
    send_ticket(ticket.id)
    image_url = ticket.ticket_image.url
    if settings.DEBUG:
        image_url = settings.TICKETIFY_API_SERVER + image_url
    return image_url
    

def generate_qr_code(ticket_id):
    # Generate the QR code using the ticket ID
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=30, border=8)
    qr.add_data(ticket_id)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Create a BytesIO object to store the image data
    qr_image_bytes = BytesIO()
    qr_image.save(qr_image_bytes, format='PNG')
    qr_image_bytes.seek(0)

    return qr_image_bytes.getvalue()

@shared_task(name="resend_email")
def send_ticket(ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    recipient_email = ticket.customer_email
    event_name = ticket.event.name
    sub_events = ticket.selected_sub_events.all().values_list('name', 'coordinator', 'coordinator_phone')
    email_data = {
        "recipient_name": ticket.customer_name,
        "doors": sub_events,
        "terms": ticket.event.terms_url,
    }
    html_content = render_to_string('email/email_template.html', email_data)
    email = EmailMultiAlternatives(f"Your ticket for {event_name}", "Please find your ticket attached", settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach_alternative(html_content, "text/html")
    image_data = ticket.ticket_image.read()
    email.attach('ticket_image.jpg', image_data, 'image/jpeg')

    # Send the email
    email.send()
    TicketEmailLog.objects.create(ticket=ticket, email_sent_time=timezone.now())
    ticket.save()
    return True


@shared_task(name="encrypt_decrypt_ticket_id")
def encrypt_decrypt_ticket_id(ticket_id, decrypt=False):
    encryption_key = os.environ.get("ENCRYPTION_KEY")
    if not encryption_key:
        # Generate a new encryption key
        encryption_key = Fernet.generate_key()
        os.environ["ENCRYPTION_KEY"] = encryption_key.decode('utf-8')
    f = Fernet(encryption_key)
    if decrypt:
        ticket_id = f.decrypt(ticket_id.encode('utf-8')).decode('utf-8')
    else:
        ticket_id = f.encrypt(ticket_id.encode('utf-8')).decode('utf-8')
    return ticket_id