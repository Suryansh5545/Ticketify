
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
from .models import Event, PromoCode, SubEvent, Addon
from ticket.models import Ticket
from .serializers import EventSerializer, SubEventSerializer, AddonSerializer


class GetActiveEvent(APIView):
    def get(self, request, format=None):
        event = Event.objects.filter(is_active=True)
        serializer = EventSerializer(event, context={"request": request}, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetSubEvent(APIView):
    def get(self, request, pk, format=None):
        event = Event.objects.get(pk=pk)
        sub_event = event.subevent_set.filter(is_active=True)
        serializer = SubEventSerializer(sub_event, context={"request": request}, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetAddon(APIView):
    def get(self, request, pk, format=None):
            event = Event.objects.get(pk=pk)
            addon = event.addon_set.filter(is_active=True)
            serializer = AddonSerializer(addon, many=True)
            if serializer.is_valid:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class ProcessPromoCode(APIView):
    def post(self, request, format=None):
        try:
            promo_code = request.data.get("promo_code")
            event_id = request.data.get("event_id")
            promo_code = PromoCode.objects.get(code=promo_code)
            event = Event.objects.get(pk=event_id)
            if promo_code.event == event:
                promo_code.stock -= 1
                return Response({"discount": promo_code.discount}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Promo code not valid for this event"}, status=status.HTTP_400_BAD_REQUEST)
        except PromoCode.DoesNotExist:
            return Response({"error": "Promo code does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        

class get_max_ticket_sales(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        tickets = Ticket.objects.filter(event=event, is_active=True)
        total_amount = 0
        for ticket in tickets:
            total_amount += ticket.transaction_id.payment_amount
        ticket_number = tickets.count()
        return Response({"total_tickets": ticket_number, "total_amount": total_amount}, status=status.HTTP_200_OK)


class get_sub_event_sales(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        sub_events = SubEvent.objects.filter(event=event)
        sub_events_sales = []
        sub_events_names = []
        for sub_event in sub_events:
            sub_event.ticket_count = Ticket.objects.filter(event=event, selected_sub_events=sub_event).count()
            sub_events_sales.append(sub_event.ticket_count)
            sub_events_names.append(sub_event.name)
        return Response({"data": sub_events_sales, "label": sub_events_names}, status=status.HTTP_200_OK)
    

class get_addon_sales(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        addons = Addon.objects.filter(event=event)
        addons_sales = []
        addons_names = []
        for addon in addons:
            addon.ticket_count = Ticket.objects.filter(event=event, selected_addons=addon).count()
            addons_sales.append(addon.ticket_count)
            addons_names.append(addon.name)
        return Response({"data": addons_sales, "label": addons_names}, status=status.HTTP_200_OK)