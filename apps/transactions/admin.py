from django.contrib import admin
from .models import Transaction
from import_export.admin import ImportExportModelAdmin

class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'payment_status', 'order_id', 'payment_id', 'payment_amount', 'webhook_recieved','created_at', 'updated_at')
    search_fields = ('id', 'payment_status', 'order_id', 'payment_id')
    list_filter = ('payment_status','webhook_recieved')

admin.site.register(Transaction, TransactionAdmin)