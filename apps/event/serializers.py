from .models import Event, SubEvent, Addon
from rest_framework import serializers
from django.conf import settings

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "name", "description", "start_date", "end_date", "image" , "location", "event_page", "price", "sub_events_included_allowed", "flagship_event_included_allowed", "payment_gateway", "terms_url", "rules_url", "student_price", "additional_info", "sponsor_logo", "maintaince_mode")

class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEvent
        fields = ("id", "name", "description", "start_date", "end_date", "image", "event", "price", "type")
    
class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ("id", "name", "icon", "event", "price", "stock")
