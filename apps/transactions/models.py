from django.db import models


class Transaction(models.Model):
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, default="")
    payment_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_currency = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    webhook_recieved = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transaction"
        ordering = ["-id"]

    def __str__(self):
        return self.order_id
