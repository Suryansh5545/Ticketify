from django.contrib import admin
from .models import Ticket, CheckIn, TicketEmailLog
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class CustomTicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
        import_id_fields = ('customer_email', 'customer_phone')
        exclude = ('id',)
        fields = ('id', 'ticket_type', 'customer_name', 'customer_email', 'customer_phone', 'customer_type', 'college_name','event', 'selected_sub_events', 'selected_addons', 'is_active', 'order_id', 'referral', 'promocode')

class CustomTicketExportResource(CustomTicketResource):
    class Meta:
        fields = ('id', 'ticket_type', 'customer_name', 'customer_email', 'customer_phone', 'customer_type', 'college_name','event', 'selected_sub_events', 'selected_addons', 'is_active', 'order_id', 'referral', 'promocode', 'transaction_id__payment_id', 'transaction_id__payment_amount')

class TicketAdmin(ImportExportModelAdmin):
    resource_class = CustomTicketResource
    list_display = ('id', 'check_in', 'customer_name', 'customer_email', 'customer_phone', 'is_active', 'ticket_image_generated', 'ticket_type', 'event', 'order_id', 'transaction_id', 'created_at', 'updated_at', 'promocode',)
    search_fields = ('id', 'check_in', 'customer_name', 'customer_email', 'customer_phone', 'ticket_type' , 'order_id', 'promocode__code')
    list_filter = ('event', 'selected_sub_events' , 'selected_addons', 'ticket_type' ,'is_active', 'ticket_image_generated')

    def get_list_display(self, request):
        # Get the default list_display for superusers
        superuser_list_display = super().get_list_display(request)
        
        # Check if the user is a superuser
        if request.user.is_superuser:
            return superuser_list_display
        else:
            # For normal staff, remove 'check_in' from the list_display
            return [field for field in superuser_list_display if field != 'check_in']
    def get_export_resource_class(self):
        return CustomTicketExportResource
        

class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
        fields = ('id', 'customer_name', 'customer_email', 'customer_phone','event', 'is_active', 'order_id', 'transaction_id__payment_id', 'transaction_id__payment_amount','created_at', 'updated_at',)
        export_order = ('id', 'customer_name', 'customer_email', 'customer_phone','event', 'is_active', 'order_id', 'transaction_id__payment_id', 'transaction_id__payment_amount','created_at', 'updated_at',)


admin.site.register(Ticket, TicketAdmin)


class CheckInAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ticket', 'check_in_time', 'operator', 'method',)
    search_fields = ('id', 'ticket', 'operator')
    list_filter = ('method',)


class CheckInResource(resources.ModelResource):
    class Meta:
        model = CheckIn
        fields = ('id', 'ticket', 'check_in_time', 'operator', 'method',)
        export_order = ('id', 'ticket', 'check_in_time', 'operator', 'method',)

admin.site.register(CheckIn, CheckInAdmin)


class TicketEmailLogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ticket', 'email_sent_time',)
    search_fields = ('id', 'ticket')


admin.site.register(TicketEmailLog, TicketEmailLogAdmin)
