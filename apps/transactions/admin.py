from django.contrib import admin
from .models import Transaction
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class TransactionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'payment_status', 'order_id', 'payment_id', 'payment_amount', 'webhook_recieved','created_at', 'updated_at')
    search_fields = ('id', 'payment_status', 'order_id', 'payment_id')
    list_filter = ('payment_status','webhook_recieved')

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('id', 'payment_status', 'order_id', 'payment_id', 'payment_amount', 'webhook_recieved','created_at', 'updated_at')
        export_order = ('id', 'payment_status', 'order_id', 'payment_id', 'payment_amount', 'webhook_recieved','created_at', 'updated_at')

admin.site.register(Transaction, TransactionAdmin)