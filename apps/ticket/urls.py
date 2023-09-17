from django.urls import path
from .views import  get_tickets_by_filter, handle_check_in, get_check_in_data, resend_email, get_ticket_by_subevents, get_ticket_by_addons, get_ticket_by_task, total_check_in_today

urlpatterns = [
    path('get_tickets_by_filter/', get_tickets_by_filter.as_view(), name='get_tickets_by_filter'),
    path('handle_check_in/', handle_check_in.as_view(), name='handle_check_in'),
    path('get_check_in_data/', get_check_in_data.as_view(), name='get_check_in_data'),
    path('resend_email/', resend_email.as_view(), name='resend_email'),
    path('get_ticket_by_subevents/', get_ticket_by_subevents.as_view(), name='get_ticket_by_subevents'),
    path('get_ticket_by_addons/', get_ticket_by_addons.as_view(), name='get_ticket_by_addons'),
    path('get_ticket_by_task/', get_ticket_by_task.as_view(), name='get_ticket_by_task'),
    path('total_check_in_today/', total_check_in_today.as_view(), name='total_check_in_today'),
]