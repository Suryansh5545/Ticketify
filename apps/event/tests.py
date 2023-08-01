from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from event.models import Event, SubEvent, Addon, PromoCode
from ticket.models import Ticket
from transactions.models import Transaction
from django.contrib.auth.models import User


class TestEvent(TestCase):
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
    def test_get_event_when_active(self):
        expected = [
            {
                "id": self.event.id,
                "name": self.event.name,
                "description": self.event.description,
                "start_date": self.event.start_date,
                "end_date": self.event.end_date,
                "image": None,
                "location": self.event.location,
                "event_page": self.event.event_page,
                "price": format(self.event.price, ".2f"),
                "sub_events_included_allowed": self.event.sub_events_included_allowed,
            }
        ]
        response = self.client.get(reverse('get_active_event'))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_event_when_inactive(self):
        self.event.is_active = False
        self.event.save()
        response = self.client.get(reverse('get_active_event'))
        self.assertEqual(response.status_code, 400)


class TestSubEvent(TestCase):
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

    def test_get_subevent_when_active(self):
        expected = [
            {
                "id": self.sub_event.id,
                "name": self.sub_event.name,
                "description": self.sub_event.description,
                "start_date": self.sub_event.start_date,
                "end_date": self.sub_event.end_date,
                "image": None,
                "event": self.sub_event.event.id,
                "price": format(self.sub_event.price, ".2f"),
            }
        ]

        response = self.client.get(reverse('get_sub_event', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_subevent_when_inactive(self):
        self.sub_event.is_active = False
        self.sub_event.save()
        response = self.client.get(reverse('get_sub_event', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, 400)


class TestAddon(TestCase):
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

        self.addon= Addon.objects.create(
            name="Hostel",
            icon="hotel",
            price=300.00,
            event=self.event,
            stock=10,
            is_active=True,
        )

    def test_get_addon_when_active(self):
        expected = [
            {
                "id": self.addon.id,
                "name": self.addon.name,
                "icon": self.addon.icon,
                "event": self.addon.event.id,
                "price": format(self.addon.price, ".2f"),
                "stock": self.addon.stock,
            }
        ]

        response = self.client.get(reverse('get_addon', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_addon_when_inactive(self):
        self.addon.is_active = False
        self.addon.save()
        response = self.client.get(reverse('get_addon', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, 400)


class TestPromoCode(TestCase):
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

        self.promo_code = PromoCode.objects.create(
            code="TEST",
            discount=10,
            event=self.event,
            stock=10,
        )

    def test_get_promo_code_when_active(self):
        expected = {
            "discount": self.promo_code.discount,
        }

        response = self.client.post(reverse('process_promo_code'), data={"promo_code": self.promo_code.code, "event_id": self.event.id})
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_promo_code_when_inactive(self):
        self.promo_code.is_active = False
        self.promo_code.save()
        response = self.client.post(reverse('process_promo_code'), data={"promo_code": self.promo_code.code, "event_id": self.event.id})
        self.assertEqual(response.status_code, 400)

    def test_get_promo_when_stock_zero(self):
        self.promo_code.stock = 0
        self.promo_code.save()
        response = self.client.post(reverse('process_promo_code'), data={"promo_code": self.promo_code.code, "event_id": self.event.id})
        self.assertEqual(response.status_code, 400)

    def test_get_promo_code_when_invalid(self):
        response = self.client.post(reverse('process_promo_code'), data={"promo_code": "INVALID", "event_id": self.event.id})
        self.assertEqual(response.status_code, 400)


class TestStats(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="example@example.com",
            password="testpassword",
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
            customer_email="example@example.com",
            customer_phone="1234567890",
            event=self.event,
            is_active=True,
            transaction_id=self.transaction,
        )

        self.ticket.selected_sub_events.set([self.sub_event])
        self.ticket.selected_addons.set([self.addon])

        self.client.force_login(self.user)

    def test_get_max_ticket_sales(self):
        expected = {
            "total_tickets": 1,
            "total_amount": Decimal(format(self.event.price + self.sub_event.price + self.addon.price , ".2f")),
        }

        response = self.client.get(reverse('get_max_ticket_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_sub_event_sales(self):
        expected = {
            "data": [1],
            "label": ["SubEvent"],
        }

        response = self.client.get(reverse('get_sub_event_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_addon_sales(self):
        expected = {
            "data": [1],
            "label": ["Hostel"],
        }

        response = self.client.get(reverse('get_addon_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_max_ticket_sales_when_no_tickets(self):
        self.ticket.delete()
        expected = {
            "total_tickets": 0,
            "total_amount": 0.00,
        }

        response = self.client.get(reverse('get_max_ticket_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_sub_event_sales_when_no_tickets(self):
        self.ticket.delete()
        expected = {
            "data": [0],
            "label": ["SubEvent"],
        }

        response = self.client.get(reverse('get_sub_event_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

    def test_get_addon_sales_when_no_tickets(self):
        self.ticket.delete()
        expected = {
            "data": [0],
            "label": ["Hostel"],
        }

        response = self.client.get(reverse('get_addon_sales', kwargs={'pk': self.event.id}))
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)

