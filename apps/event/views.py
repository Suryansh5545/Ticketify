
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
from .models import Event, PromoCode, SubEvent, Addon
from ticket.models import Ticket
from .serializers import EventSerializer, SubEventSerializer, AddonSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

class GetActiveEvent(ListAPIView):
    """
    Get all active events
    """
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        if self.queryset.exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response("No Active Event", status=status.HTTP_400_BAD_REQUEST)

    
class GetSubEvent(APIView):
    """
    Get all active sub events
    """
    def get(self, request, pk, format=None):
        event = Event.objects.get(pk=pk)
        sub_event = event.subevent_set.filter(is_active=True)
        if sub_event:
            serializer = SubEventSerializer(sub_event, context={"request": request}, many=True)
            if serializer.is_valid:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No Active Sub Event", status=status.HTTP_400_BAD_REQUEST)
        
class GetAddon(APIView):
    """
    Get all active addons
    """
    def get(self, request, pk, format=None):
            event = Event.objects.get(pk=pk)
            addon = event.addon_set.filter(is_active=True)
            if addon:
                serializer = AddonSerializer(addon, many=True)
                if serializer.is_valid:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("No active Addon", status=status.HTTP_400_BAD_REQUEST)
            
class ProcessPromoCode(APIView):
    """
    Process Promo Code
    """
    def post(self, request, format=None):
        try:
            promo_code = request.data.get("promo_code")
            event_id = request.data.get("event_id")
            promo_code = PromoCode.objects.get(code__iexact=promo_code,is_active=True)
            if promo_code.stock == 0:
                return Response({"error": "Promo code out of stock"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                event = Event.objects.get(pk=event_id)
                if promo_code.event == event:
                    return Response({"discount": promo_code.discount}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Promo code not valid for this event"}, status=status.HTTP_400_BAD_REQUEST)
        except PromoCode.DoesNotExist:
            return Response({"error": "Promo code does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        

class get_max_ticket_sales(APIView):
    """
    Get max ticket sales
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        tickets = Ticket.objects.filter(event=event, is_active=True, ticket_type='REGULAR')
        total_amount = 0
        for ticket in tickets:
            total_amount += ticket.transaction_id.payment_amount
        ticket_number = tickets.count()
        return Response({"total_tickets": ticket_number, "total_amount": total_amount}, status=status.HTTP_200_OK)


class get_sub_event_sales(APIView):
    """
    Get sub event sales
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        sub_events = SubEvent.objects.filter(event=event)
        sub_events_sales = []
        sub_events_names = []
        for sub_event in sub_events:
            sub_event.ticket_count = Ticket.objects.filter(event=event, selected_sub_events=sub_event, is_active=True).count()
            sub_events_sales.append(sub_event.ticket_count)
            sub_events_names.append(sub_event.name)
        return Response({"data": sub_events_sales, "label": sub_events_names}, status=status.HTTP_200_OK)
    

class get_addon_sales(APIView):
    """
    Get addon sales
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
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