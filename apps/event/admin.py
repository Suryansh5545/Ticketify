from django.contrib import admin
from .models import Event, SubEvent, Addon, PromoCode
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class SubEventAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'event', 'is_active')
    search_fields = ('name', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', )


class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'stock', 'is_active')
    search_fields = ('name', )

class CustomTicketResource(resources.ModelResource):
    class Meta:
        model = PromoCode
        import_id_fields = ('email', 'name')
        exclude = ('id','code')
        fields = ('code','event', 'stock', 'is_active', 'email', 'name', 'discount')
        export_order = ('event', 'stock', 'is_active', 'email', 'name', 'discount')


class PromoCodeAdmin(ImportExportModelAdmin):
    resource_class = CustomTicketResource
    list_display = ('code', 'event', 'stock', 'is_active', 'name', 'email', 'email_sended')
    search_fields = ('code', 'name', 'email')


admin.site.register(Event, EventAdmin)
admin.site.register(SubEvent, SubEventAdmin)
admin.site.register(Addon, AddonAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
