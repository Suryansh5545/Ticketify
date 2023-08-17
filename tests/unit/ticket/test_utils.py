from ticket.utils import generate_ticket_image, create_ticket, generate_qr_code, encrypt_decrypt_ticket_id
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ticket.models import Ticket
from unittest.mock import patch
from event.models import Event, SubEvent, Addon


class TestCreateTicket(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
                name="Event",
                description="Test Event",
                start_date="2023-09-26",
                end_date="2023-09-29",
                location="Test",
                price=300.00,
                sub_events_included_allowed=3,
                is_active=True,
                event_page="",
            )
        self.sub_event = SubEvent.objects.create(
            name="SubEvent",
            description="This is a sub event of Event",
            start_date="2023-09-26",
            end_date="2020-09-29",
            price=100.00,
            event=self.event,
            is_active=True,
        )

        self.addon = Addon.objects.create(
            name="Hostel",
            icon="hotel",
            price=300.00,
            event=self.event,
            stock=10,
            is_active=True,
        )

    def test_create_ticket(self):
        order_id = 1
        request_data = {
            "customer_name": "Test User",
            "customer_email": "example@example.com",
            "customer_phone": "1234567890",
            "referral": "Test Referral",
            "event_id": self.event.id,
            "selected_sub_events": [self.sub_event.id],
            "selected_addons": [self.addon.id],
        }
        factory = APIRequestFactory()
        request = factory.post('/create_ticket/')
        request.data = request_data
        create_ticket(request, order_id)

        # Check that the ticket was created successfully
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.customer_name, request_data["customer_name"])
        self.assertEqual(ticket.customer_email, request_data["customer_email"])
        self.assertEqual(ticket.customer_phone, request_data["customer_phone"])
        self.assertEqual(ticket.referral, request_data["referral"])
        self.assertEqual(ticket.event_id, request_data["event_id"])
        self.assertEqual(ticket.selected_sub_events.count(), 1)
        self.assertEqual(ticket.selected_addons.count(), 1)
        self.assertEqual(int(ticket.order_id), order_id)


# class TestGenerateTicketImage(TestCase):
#     @patch("ticket.utils.imgkit")
#     @patch("ticket.utils.send_ticket")
#     @patch("ticket.utils.io.BytesIO")
#     def test_generate_ticket_image(self, mock_imgkit, mock_send_ticket, mock_bytes_io):
#         self.event = Event.objects.create(
#             name="Event",
#             description="Test Event",
#             start_date="2023-09-26",
#             end_date="2023-09-29",
#             location="Test",
#             price=300.00,
#             sub_events_included_allowed=3,
#             is_active=True,
#             event_page="",
#         )
#         self.ticket = Ticket.objects.create(
#             customer_name="Test User",
#             customer_email="example@email.com",
#             customer_phone="1234567890",
#             event_id=1,
#         )
#         mock_imgkit.from_string.return_value = None
#         mock_send_ticket.return_value = None
#         mock_bytes_io.return_value = None
#         generate_ticket_image(self.ticket.id)
#         self.assertNotEqual(self.ticket.ticket_image, None)


class TestGenerateQRCode(TestCase):
    def test_generate_qr_code(self):
        ticket_id = 14323
        qr_code_image = generate_qr_code(ticket_id)
        self.assertNotEqual(qr_code_image, None)


class TestEncryptDecryptTicketId(TestCase):
    def test_encrypt_decrypt_ticket_id(self):
        ticket_id = 'DFGN45'
        encrypted_ticket_id = encrypt_decrypt_ticket_id(ticket_id)
        self.assertNotEqual(encrypted_ticket_id, None)
        decrypted_ticket_id = encrypt_decrypt_ticket_id(encrypted_ticket_id, True)
        self.assertEqual(decrypted_ticket_id, ticket_id)