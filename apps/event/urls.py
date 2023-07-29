from django.urls import path
from .views import GetActiveEvent, GetSubEvent, GetAddon, ProcessPromoCode, get_max_ticket_sales, get_sub_event_sales, get_addon_sales

urlpatterns = [
    path('get_event/', GetActiveEvent.as_view(), name='get_active_event'),
    path('get_sub_event/<int:pk>/', GetSubEvent.as_view(), name='get_sub_event'),
    path('get_addon/<int:pk>/', GetAddon.as_view(), name='get_addon'),
    path('process_promo_code/', ProcessPromoCode.as_view(), name='process_promo_code'),
    path('get_max_ticket_sales/<int:pk>/', get_max_ticket_sales.as_view(), name='get_max_ticket_sales'),
    path('get_sub_event_sales/<int:pk>/', get_sub_event_sales.as_view(), name='get_sub_event_sales'),
    path('get_addon_sales/<int:pk>/', get_addon_sales.as_view(), name='get_addon_sales'),
]