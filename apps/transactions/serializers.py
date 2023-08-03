from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('payment_method', 'payment_status', 'order_id', 'payment_id', 'payment_amount', 'payment_currency')