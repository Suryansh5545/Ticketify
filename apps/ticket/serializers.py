from rest_framework import serializers
from event.serializers import SubEventSerializer, AddonSerializer
from transactions.serializers import TransactionSerializer

class TicketSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    referral = serializers.CharField(required=False, allow_blank=True)
    event_id = serializers.IntegerField()
    selected_sub_events = serializers.ListField(child=serializers.IntegerField(), required=False)
    selected_addons = serializers.ListField(child=serializers.IntegerField(), required=False)


class AdminTicketSerializer(serializers.Serializer):
    id = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField()
    event_id = serializers.IntegerField()
    selected_sub_events = SubEventSerializer(many=True, required=False)
    selected_addons = AddonSerializer(many=True, required=False)
    transaction_id = TransactionSerializer(required=True)


class CheckInSerializer(serializers.Serializer):
    ticket_id = serializers.CharField()
    check_in_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p")
    operator = serializers.CharField()
    method = serializers.CharField()

class TicketListSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    customer_phone = serializers.CharField()