import datetime
from event.models import SubEvent, Addon
from .models import Ticket, CheckIn
from rest_framework.views import APIView, Response
from .serializers import AdminTicketSerializer, CheckInSerializer, TicketListSerializer, TicketListSerializerExcel, TicketSerializerExcel, TicketVerify
from django.db.models import Q
from rest_framework import permissions, status, authentication
from .utils import generate_ticket_image, send_ticket
from celery.result import AsyncResult
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from rest_framework_simplejwt.authentication import JWTAuthentication

    

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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        name = request.data.get('name')
        referral = request.data.get('referral')
        ticket_id = request.data.get('ticket_id')
        if ticket_id:
            try:
                ticket = Ticket.objects.get(check_in=ticket_id, is_active=True)
            except Ticket.DoesNotExist:
                return Response({"message": "Ticket does not exist or isn't active"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = AdminTicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if not email and not phone and not name and not referral:
                return Response({"message": "At least one of email, phone or name or referral is required"}, status=status.HTTP_400_BAD_REQUEST)
            query = Q()
            if email:
                query &= Q(customer_email__icontains=email)

            if phone:
                query &= Q(customer_phone__icontains=phone)

            if name:
                query &= Q(customer_name__icontains=name)
            
            if referral:
                query &= Q(referral__icontains=referral)

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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self, request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
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
            elif ticket.customer_type == "SCHOOL":
                if ticket.id_verified == True:
                    generate_ticket_image.delay(ticket.id)
                else:
                    return Response({"message": "Ticket is not verified"}, status=status.HTTP_400_BAD_REQUEST)
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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self, request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
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
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
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
        

class get_unverified_ticket_by_time(APIView):
    """
    Get unverified tickets in time order
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def get(self, request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        tickets = Ticket.objects.filter(is_active=True, customer_type="SCHOOL", id_verified=False, declined=False).order_by('created_at')
        if not tickets:
            return Response({"message": "No unverified tickets left"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TicketVerify(tickets, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class verify_ticket(APIView):
    """
    Verify a ticket
    Query Parameters:
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self,request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"message": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.is_active:
            ticket.id_verified = True
            ticket.save()
            if ticket.ticket_image_generated == False:
                generate_ticket_image.delay(ticket.id)
            return Response({"message": "Ticket verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ticket is not active"}, status=status.HTTP_400_BAD_REQUEST)
        

class total_check_in_today(APIView):
    """
    Get total check ins today"""
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self, request):
        time = datetime.datetime.now()
        total = CheckIn.objects.filter(check_in_time__date=time.date()).count()
        return Response({"total": total}, status=status.HTTP_200_OK)
    

class get_ticket_by_subevents_excel_download(APIView):
    """
    Get tickets by sub events
    Query Parameters:
    list_id: ID of the sub event
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def get(self, request, pk):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        if not pk:
            return Response({"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif SubEvent.objects.filter(id=pk, is_active=True).exists() == False:
            return Response({"message": "Sub Event does not exist or is not active"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tickets = Ticket.objects.filter(selected_sub_events__in=[pk], is_active=True)
            sub_event_name = SubEvent.objects.get(id=pk).name
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if tickets.exists():
            serializer = TicketListSerializerExcel(tickets, many=True)
            wb = Workbook()
            ws = wb.active
            ws.title = "Tickets"

            # Iterate through the serialized data and write it to the worksheet
            for index, data in enumerate(serializer.data):
                if index == 0:
                    # Write header row
                    headers = list(data.keys())
                    ws.append(headers)
                row_data = list(data.values())
                ws.append(row_data)

            excel_data = BytesIO()
            wb.save(excel_data)

            # Create a response with the Excel file
            response = HttpResponse(
                content=excel_data.getvalue(),
                content_type="application/ms-excel",
            )
            response["Content-Disposition"] = "attachment; filename=sub_event_"+sub_event_name+"_tickets.xlsx"

            return response
        else:
            return Response({"message": "No tickets found"}, status=status.HTTP_400_BAD_REQUEST)
        

class get_all_tickets_excel(APIView):
    """
    Get all tickets
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def get(self, request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        tickets = Ticket.objects.filter(is_active=True)
        if tickets.exists():
            serializer = TicketSerializerExcel(tickets, many=True)
            wb = Workbook()
            ws = wb.active
            ws.title = "Tickets"

            # Iterate through the serialized data and write it to the worksheet
            for index, data in enumerate(serializer.data):
                if index == 0:
                    # Write header row
                    headers = list(data.keys())
                    ws.append(headers)
                row_data = list(data.values())
                ws.append(row_data)

            excel_data = BytesIO()
            wb.save(excel_data)

            # Create a response with the Excel file
            response = HttpResponse(
                content=excel_data.getvalue(),
                content_type="application/ms-excel",
            )
            response["Content-Disposition"] = "attachment; filename=all_tickets "+ str(datetime.datetime.now()) + ".xlsx"

            return response
        else:
            return Response({"message": "No tickets found"}, status=status.HTTP_400_BAD_REQUEST)
        

class decline_verify_ticket(APIView):
    """
    Decline a ticket
    Query Parameters:
    ticket_id: ID of the ticket
    """
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]
    def post(self,request):
        if request.user.is_staff == False:
            return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        ticket_id = request.data.get('ticket_id')
        if not ticket_id:
            return Response({"message": "ticket_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id, is_active=True)
        except Ticket.DoesNotExist:
            return Response({"message": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if ticket.is_active:
            ticket.declined = True
            ticket.save()
            return Response({"message": "Ticket declined successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ticket is not active"}, status=status.HTTP_400_BAD_REQUEST)

