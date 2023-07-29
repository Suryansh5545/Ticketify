from django.contrib import admin
from .models import Event, SubEvent, Addon, PromoCode
from import_export.admin import ImportExportModelAdmin

class SubEventAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'event', 'is_active')
    search_fields = ('name', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', )


class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'stock', 'is_active')
    search_fields = ('name', )


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'event', 'stock', 'is_active')
    search_fields = ('code', )


admin.site.register(Event, EventAdmin)
admin.site.register(SubEvent, SubEventAdmin)
admin.site.register(Addon, AddonAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
