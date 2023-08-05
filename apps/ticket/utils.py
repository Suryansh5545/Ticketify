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
from event.models import Event
from django.conf import settings


def create_ticket(request, order_id):
        if request.method == "POST":
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                customer_name = validated_data['customer_name']
                customer_email = validated_data['customer_email']
                customer_phone = validated_data['customer_phone']
                event_id = validated_data['event_id']
                selected_sub_events = validated_data.get('selected_sub_events', [])
                selected_addons = validated_data.get('selected_addons', [])
                event = Event.objects.get(pk=event_id)
                ticket = Ticket.objects.create(
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    event=event,order_id = order_id
                )
                ticket.selected_sub_events.set(selected_sub_events)
                ticket.selected_addons.set(selected_addons)
                ticket.save()
            else:
                raise Exception(serializer.errors)


@shared_task(name="generate_ticket_image")
def generate_ticket_image (ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    encrypted_ticket_id = encrypt_decrypt_ticket_id(ticket.id)
    qr_code_image = generate_qr_code(ticket.check_in)
    qr_code_image_base64 = base64.b64encode(qr_code_image).decode('utf-8')
    sub_events = ticket.selected_sub_events.all().values_list('name', flat=True)
    ticket_data = {
            "spam": "",
            "ticketNumber": ticket.id,
            "artistName": ticket.customer_name,
            "showName": ticket.event.name,
            "location": ticket.event.location,
            "day": ticket.event.start_date.strftime("%A"),
            "date": ticket.event.start_date.strftime("%B %d") + " - " + ticket.event.end_date.strftime("%d"),
            "year": ticket.event.start_date.strftime("%Y"),
            "timeSlot": ticket.event.start_date.strftime("%I:%M %p") + " TO " + ticket.event.end_date.strftime("%I:%M %p"),
            "doors": sub_events,
            "barcodeImageURL": f"data:image/png;base64,{qr_code_image_base64}",
        }

    template = get_template('ticket/ticket_template.html')
    html_content = template.render(ticket_data)
    options = {
        'width': '802',
        'height': '250',
        'quality': 100,
        'zoom': '2.0',
    }
    ticket_name = f"ticket_{encrypted_ticket_id}.jpg"
    tickets_dir = os.path.join(settings.MEDIA_ROOT, 'tickets')
    if not os.path.exists(tickets_dir):
        # Create the 'tickets' directory if it doesn't exist
        os.makedirs(tickets_dir)
    image_path = os.path.join(settings.MEDIA_ROOT, 'tickets', ticket_name)
    imgkit.from_string(html_content, image_path, options=options)
    ticket.ticket_image_location = image_path
    ticket.save()
    send_ticket(ticket.id)
    image_url = f"{settings.TICKETIFY_API_SERVER}{settings.MEDIA_URL}{'tickets/'}{ticket_name}"
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
    image_path = ticket.ticket_image_location
    # Create the email message
    email = EmailMultiAlternatives(f"Your ticket for {event_name}", "Please find your ticket attached", settings.DEFAULT_FROM_EMAIL, [recipient_email])

    # Attach the image to the email
    with open(image_path, 'rb') as f:
        email.attach('ticket_image.jpg', f.read(), 'image/jpeg')

    # Send the email
    email.send()
    ticket_send_log = TicketEmailLog.objects.create(ticket=ticket, email_sent_time=timezone.now())
    ticket.ticket_mail_log.set([ticket_send_log])
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