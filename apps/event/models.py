from django.db import models
from transactions.models import PaymentAggregator


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='event', blank=True)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_events_included_allowed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    event_page = models.URLField(max_length=200, blank=True)
    payment_gateway = models.ForeignKey(PaymentAggregator, default="razorpay", on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
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
    

class PromoCode(models.Model):
    code = models.CharField(max_length=30)
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "promo_code"
        ordering = ["-created_at"]

    def __str__(self):
        return self.code
