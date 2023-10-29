from django.db import models
from event.models import Event, SubEvent, Addon
from transactions.models import Transaction
import random
import string

def generate_id():
    # Generate a random 10-digit alphanumeric string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

class Ticket(models.Model):
    id = models.CharField(primary_key=True, default=generate_id, editable=False, max_length=7)
    check_in = models.CharField(editable=False, max_length=10, unique=True)
    type_options = (
        ('REGULAR', 'Regular'),
        ('STUDENT', 'Student'),
    )
    ticket_type = models.CharField(max_length=100, choices=type_options, default='REGULAR')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=100)
    types = (
        ('SCHOOL', 'School'),
        ('COLLEGE', 'College'),
    )
    customer_type = models.CharField(max_length=100, choices=types, default='COLLEGE')
    college_name = models.CharField(max_length=100, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    selected_sub_events = models.ManyToManyField(SubEvent, blank=True)
    selected_addons = models.ManyToManyField(Addon, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_image_generated = models.BooleanField(default=False)
    ticket_image = models.ImageField(upload_to='ticket_images', null=True, blank=True)
    order_id = models.CharField(max_length=100, default="", unique=True, null=True)
    transaction_id = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    referral = models.CharField(max_length=100, null=True, blank=True)
    promo_applied = models.BooleanField(default=False)
    verification_id = models.ImageField(upload_to='verification_images', null=True, blank=True)
    id_verified = models.BooleanField(default=False)
    promocode = models.ForeignKey('event.PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    declined = models.BooleanField(default=False)
    vip = models.BooleanField(default=False)

    def generate_unique_ticket_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def save(self, *args, **kwargs):
        if self.ticket_type == 'REGULAR':
            if self.transaction_id == None:
                self.is_active = False
            elif self.transaction_id.payment_id == None:
                self.is_active = False
            elif self.transaction_id.payment_status != 'captured':
                self.is_active = False
        if not self.check_in:
            # Generate a unique check_in value if it doesn't exist
            self.check_in = self.generate_unique_ticket_id()
            while Ticket.objects.filter(check_in=self.check_in).exists():
                # Regenerate the check_in value until it becomes unique
                self.check_in = self.generate_unique_ticket_id()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "ticket"
        ordering = ["-created_at"]

    def __str__(self):
        return self.customer_name
    

class CheckIn(models.Model):
    
    CHECK_IN_METHODS = (
        ('QR', 'QR Code'),
        ('MANUAL', 'Manual'),
    )

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_check_in")
    check_in_time = models.DateTimeField(auto_now_add=True)
    operator = models.CharField(max_length=100, blank=True, null=True)
    method = models.CharField(max_length=100, choices=CHECK_IN_METHODS, default='QR')

    class Meta:
        db_table = "check_in"
        ordering = ["-check_in_time"]

    def __str__(self):
        return self.ticket.customer_name
    

class TicketEmailLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_email_logs')
    email_sent_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ticket_email_log"
        ordering = ["-email_sent_time"]

    def __str__(self):
        return str(self.ticket) + ' ' + str(self.email_sent_time)