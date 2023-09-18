import datetime
from event.models import SubEvent, Addon
from .models import Ticket, CheckIn
from rest_framework.views import APIView, Response
from .serializers import AdminTicketSerializer, CheckInSerializer, TicketListSerializer
from django.db.models import Q
from rest_framework import permissions, status, authentication
from .utils import generate_ticket_image, send_ticket
from celery.result import AsyncResult

    

class get_tickets_by_filter(APIView):
    """
    Get tickets by email, phone or name
    Query Parameters:
    email: Email of the customer
    phone: Phone number of the customer
    name: Name of the customer
    or 
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        name = request.data.get('name')
        ticket_id = request.data.get('ticket_id')
        if ticket_id:
            try:
                ticket = Ticket.objects.get(check_in=ticket_id, is_active=True)
            except Ticket.DoesNotExist:
                return Response({"message": "Ticket does not exist or isn't active"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = AdminTicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if not email and not phone and not name:
                return Response({"message": "At least one of email, phone or name is required"}, status=status.HTTP_400_BAD_REQUEST)
            query = Q()
            if email:
                query &= Q(customer_email__icontains=email)

            if phone:
                query &= Q(customer_phone__icontains=phone)

            if name:
                query &= Q(customer_name__icontains=name)

            tickets = Ticket.objects.filter(query, is_active=True)
            if not tickets.exists():
                return Response({"message": "No tickets found"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = AdminTicketSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    

class handle_check_in(APIView):
    """
    Check in a ticket
    Query Parameters:
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"message": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        operator = request.user.username
        if len(ticket_id) == 10:
            method = "QR"
        else:
            method = "MANUAL"
        time = datetime.datetime.now()
        if not ticket_id or not operator or not method:
            return Response({"message": "ticket_id, operator and method are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if(method == "QR"):
                ticket = Ticket.objects.get(check_in=ticket_id, is_active=True)
            else:
                ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist or is not active"}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.event.end_date < time.date():
            return Response({"message": "Event has ended"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if ticket.is_active:
                check_in_check = CheckIn.objects.filter(ticket=ticket, check_in_time__date=time.date())
                if check_in_check.exists():
                    return Response({"message": "Ticket already checked in today"}, status=status.HTTP_400_BAD_REQUEST)
                
                CheckIn.objects.create(ticket=ticket, operator=operator, method=method)
                return Response({"message": "Ticket checked in successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Ticket is not active"}, status=status.HTTP_400_BAD_REQUEST)
            

class get_check_in_data(APIView):
    """
    Get check in data of a ticket
    Query Parameters:
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"message": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.is_active:
            check_in = CheckIn.objects.filter(ticket=ticket)
            if check_in.exists():
                serializer = CheckInSerializer(check_in, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Ticket has not been checked in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Ticket is not active"}, status=status.HTTP_400_BAD_REQUEST)
        

class resend_email(APIView):
    """
    Resend ticket email
    Query Parameters:
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"message": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.is_active:
            if ticket.ticket_image:
                send_ticket.delay(ticket.id)
            else:
                generate_ticket_image.delay(ticket.id)
            return Response({"message": "Ticket email sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ticket is not active"}, status=status.HTTP_400_BAD_REQUEST)
        

class get_ticket_by_subevents(APIView):
    """
    Get tickets by sub events
    Query Parameters:
    list_id: ID of the sub event
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        list_id = request.data.get('list_id')
        if not list_id:
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif SubEvent.objects.filter(id=list_id, is_active=True).exists() == False:
            return Response({"message": "Sub Event does not exist or is not active"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tickets = Ticket.objects.filter(selected_sub_events__in=[list_id], is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if tickets.exists():
            serializer = TicketListSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No tickets found"}, status=status.HTTP_400_BAD_REQUEST)        
        

class get_ticket_by_addons(APIView):
    """
    Get tickets by addons
    Query Parameters:
    list_id: ID of the addon
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        list_id = request.data.get('list_id')
        if not list_id:
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif Addon.objects.filter(id=list_id, is_active=True).exists() == False:
            return Response({"message": "Sub Event does not exist or is not active"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tickets = Ticket.objects.filter(selected_addons__in=[list_id], is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if tickets.exists():
            serializer = TicketListSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No tickets found"}, status=status.HTTP_400_BAD_REQUEST)
        

class get_ticket_by_task(APIView):
    def post(self, request):
        task_id = request.data.get('task_id')
        if not task_id:
            return Response({"message": "task_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = AsyncResult(task_id)
        except:
            return Response({"message": "Task does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if result.status == "SUCCESS":
            return Response(result.result, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Task is not complete"}, status=status.HTTP_400_BAD_REQUEST)
        

class total_check_in_today(APIView):
    """
    Get total check ins today"""
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication]
    def post(self, request):
        time = datetime.datetime.now()
        total = CheckIn.objects.filter(check_in_time__date=time.date()).count()
        return Response({"total": total}, status=status.HTTP_200_OK)

