import datetime
from unittest.mock import patch
from django.test import TestCase
from event.models import Event, SubEvent, Addon
from ticket.models import Ticket, CheckIn
from transactions.models import Transaction
from django.contrib.auth.models import User
from django.utils.timezone import make_aware


class TestTicket(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
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
        self.transaction = Transaction.objects.create(
            payment_method="upi",
            payment_status="captured",
            order_id="1234567890",
            payment_id="1234567890",
            payment_amount=self.event.price + self.sub_event.price + self.addon.price,
            payment_currency="INR",
        )
        self.ticket = Ticket.objects.create(
            customer_name="Test User",
            customer_email="example@email.com",
            customer_phone="1234567890",
            event_id=1,
            is_active=True,
            check_in="1234567890",
            transaction_id=self.transaction,
        )
        self.ticket.selected_sub_events.add(self.sub_event)
        self.ticket.selected_addons.add(self.addon)

    def test_get_tickets_by_filter_without_ticket_id(self):
        self.client.force_login(self.user)

        request = self.client.post(
            "/api/ticket/get_tickets_by_filter/",
            {
                "email": self.ticket.customer_email,
                "phone": self.ticket.customer_phone,
                "name": self.ticket.customer_name,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_get_tickets_by_filter_with_ticket_id(self):
        self.client.force_login(self.user)

        request = self.client.post(
            "/api/ticket/get_tickets_by_filter/",
            {
                "ticket_id": self.ticket.check_in,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_get_tickets_by_filter_with_in_active_ticket(self):
        self.client.force_login(self.user)
        self.ticket.is_active = False
        self.ticket.save()
        request = self.client.post(
            "/api/ticket/get_tickets_by_filter/",
            {
                "email": self.ticket.customer_email,
                "phone": self.ticket.customer_phone,
                "name": self.ticket.customer_name,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.ticket.is_active = True
        self.ticket.save()

    def test_handle_check_in_with_qr(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.check_in,
                "operator": self.user.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_handle_check_in_with_manual(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_handle_check_in_with_invalid_ticket_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": "123456789s0",
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_handle_check_in_with_inactive_ticket(self):
        self.client.force_login(self.user)
        self.ticket.is_active = False
        self.ticket.save()
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.ticket.is_active = True
        self.ticket.save()

    def test_handle_check_in_with_event_ended(self):
        self.client.force_login(self.user)
        self.event.end_date = "2020-09-29"
        self.event.save()
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.event.end_date = "2023-09-29"
        self.event.save()

    def test_handle_check_in_already_check_in_for_the_day(self):
        self.client.force_login(self.user)
        CheckIn.objects.create(
            ticket=self.ticket,
            operator=self.user.id,
            method="QR",
            check_in_time=datetime.datetime.now(),
        )
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_handle_check_in_other_day_check_in(self):
        self.client.force_login(self.user)
        past_date = datetime.datetime.now() - datetime.timedelta(days=1)
        past_date_aware = make_aware(past_date)
        with patch('django.utils.timezone.now', return_value=past_date_aware):
            CheckIn.objects.create(
                ticket=self.ticket,
                operator=self.user.id,
                method="QR",
            )
        request = self.client.post(
            "/api/ticket/handle_check_in/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_handle_check_in_with_no_ticket_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/handle_check_in/",
        )
        self.assertEqual(request.status_code, 400)

    def test_get_check_in_data(self):
        self.client.force_login(self.user)
        CheckIn.objects.create(
                ticket=self.ticket,
                operator=self.user.id,
                method="QR",
            )
        request = self.client.post(
            "/api/ticket/get_check_in_data/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_get_check_in_data_with_no_ticket_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_check_in_data/",
        )
        self.assertEqual(request.status_code, 400)

    def test_get_check_in_data_with_invalid_ticket_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_check_in_data/",
            {
                "ticket_id": "1234567890",
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_get_check_in_data_with_no_check_in(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_check_in_data/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_get_check_in_data_with_inactive_ticket(self):
        self.client.force_login(self.user)
        self.ticket.is_active = False
        self.ticket.save()
        request = self.client.post(
            "/api/ticket/get_check_in_data/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.ticket.is_active = True
        self.ticket.save()

    def test_resend_ticket_email(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/resend_email/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_resend_ticket_email_with_invalid_ticket_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/resend_email/",
            {
                "ticket_id": "1234567890",
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_resend_ticket_email_with_inactive_ticket(self):
        self.client.force_login(self.user)
        self.ticket.is_active = False
        self.ticket.save()
        request = self.client.post(
            "/api/ticket/resend_email/",
            {
                "ticket_id": self.ticket.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.ticket.is_active = True
        self.ticket.save()

    def test_get_ticket_by_subevents(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_ticket_by_subevents/",
            {
                "list_id": self.sub_event.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_get_ticket_by_subevents_with_invalid_subevent_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_ticket_by_subevents/",
            {
                "list_id": "1234567890",
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_get_ticket_by_subevents_with_inactive_subevent(self):
        self.client.force_login(self.user)
        self.sub_event.is_active = False
        self.sub_event.save()
        request = self.client.post(
            "/api/ticket/get_ticket_by_subevents/",
            {
                "list_id": self.sub_event.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.sub_event.is_active = True
        self.sub_event.save()

    def test_get_ticket_by_addons(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_ticket_by_addons/",
            {
                "list_id": self.addon.id,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_get_ticket_by_addons_with_invalid_addon_id(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/api/ticket/get_ticket_by_addons/",
            {
                "list_id": "1234567890",
            },
        )
        self.assertEqual(request.status_code, 400)

    def test_get_ticket_by_addons_with_inactive_addon(self):
        self.client.force_login(self.user)
        self.addon.is_active = False
        self.addon.save()
        request = self.client.post(
            "/api/ticket/get_ticket_by_addons/",
            {
                "list_id": self.addon.id,
            },
        )
        self.assertEqual(request.status_code, 400)
    
        self.addon.is_active = True
        self.addon.save()

    
        