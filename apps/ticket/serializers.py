from rest_framework import serializers
from event.serializers import SubEventSerializer, AddonSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

class SelectedSubEventSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class TicketSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    customer_type = serializers.CharField()
    college_name = serializers.CharField(required=False, allow_blank=True)
    verification_id = serializers.CharField(required=False, allow_blank=True)
    referral = serializers.CharField(required=False, allow_blank=True)
    event_id = serializers.IntegerField()
    selected_sub_events = SelectedSubEventSerializer(many=True, required=False)
    selected_addons = serializers.ListField(child=serializers.IntegerField(), required=False)
    coupon = serializers.CharField(required=False, allow_blank=True)



class AdminTicketSerializer(serializers.Serializer):
    id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    event_id = serializers.IntegerField()
    selected_sub_events = SubEventSerializer(many=True, required=False)
    selected_addons = AddonSerializer(many=True, required=False)
    transaction_id = TransactionSerializer(required=True)
    referral = serializers.CharField(required=False, allow_blank=True)
    vip = serializers.BooleanField(default=False)


class CheckInSerializer(serializers.Serializer):
    ticket_id = serializers.CharField()
    check_in_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
    operator = serializers.CharField()
    method = serializers.CharField()

class TicketListSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_phone = serializers.CharField()

class TicketListSerializerExcel(serializers.Serializer):
    id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    referral = serializers.CharField(required=False, allow_blank=True)


class TransactionExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('payment_amount',)

class TicketSerializerExcel(serializers.Serializer):
    id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    college_name = serializers.CharField()
    referral = serializers.CharField(required=False, allow_blank=True)
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='transaction_id.payment_amount',allow_null=True)

class TicketVerify(serializers.Serializer):
    id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    event_id = serializers.IntegerField()
    selected_sub_events = SubEventSerializer(many=True, required=False)
    selected_addons = AddonSerializer(many=True, required=False)
    transaction_id = TransactionSerializer(required=True)
    referral = serializers.CharField(required=False, allow_blank=True)
    verification_id = serializers.ImageField()