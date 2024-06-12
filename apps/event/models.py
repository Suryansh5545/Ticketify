import random
import string
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='event', blank=True)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    student_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_events_included_allowed = models.IntegerField(default=0)
    flagship_event_included_allowed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    event_page = models.URLField(max_length=200, blank=True)
    pg_options = (
        ('razorpay', 'Razorpay'),
        ('billdesk', 'Billdesk'),
    )
    payment_gateway = models.CharField(max_length=100, choices=pg_options, null=True, blank=True)
    terms_url = models.URLField(max_length=200, blank=True)
    rules_url = models.URLField(max_length=200, blank=True)
    additional_info = models.TextField(blank=True)
    sponsor_logo = models.ImageField(upload_to='event', blank=True)
    maintaince_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    template_options = (
        ('sabrang', 'SABRANG'),
        ('testing', 'TESTING')
    )
    ticket_template = models.CharField(max_length=100,choices=template_options, default='testing')


    def save(self, *args, **kwargs):
        if self.is_active:
            # If this event is set to active, deactivate all other events
            Event.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


    class Meta:
        db_table = "event"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class SubEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='sub_event', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type_options = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('student', 'Student')
    )
    type = models.CharField(max_length=100, choices=type_options, default='standard')
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
    coordinator = models.CharField(max_length=100, blank=True)
    coordinator_phone = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "sub_event"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Addon(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=30, blank=True, help_text = "Font Awesome Icon Name")
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addon"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

def generate_id():
    # Generate a random 10-digit alphanumeric string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class PromoCode(models.Model):
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=10, unique=True, default=generate_id)
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=1)
    email_sended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "promo_code"
        ordering = ["-created_at"]

    def __str__(self):
        return self.code
