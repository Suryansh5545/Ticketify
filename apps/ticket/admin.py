from django.contrib import admin
from .models import Ticket, CheckIn, TicketEmailLog
from import_export.admin import ImportExportModelAdmin

class TicketAdmin(ImportExportModelAdmin):
    list_display = ('id', 'check_in', 'customer_name', 'customer_email', 'customer_phone','event', 'is_active', 'order_id', 'transaction_id', 'created_at', 'updated_at',)
    search_fields = ('id', 'check_in', 'customer_name', 'customer_email', 'customer_phone', 'order_id')
    list_filter = ('event', 'selected_sub_events' , 'selected_addons','is_active')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(CheckIn)
admin.site.register(TicketEmailLog)
