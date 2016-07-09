from django.contrib import admin

# Register your models here.
from tickets.models import *


def close_ticket(modeladmin, request, queryset):
    queryset.update(status="CLOSED")


close_ticket.short_description = "Sluit geselecteerde ticket"


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'title', 'creator', 'assigned_to', 'created_at', 'time_open')
    list_filter = ('status', 'assigned', 'created_at', 'assignment_date')
    actions = [close_ticket]
    # fieldsets = ((None, {'fields': ('ticket_type', 'creator', 'title', 'item', 'status', 'assigned')}
    #               ),
    #              ('Advanced options', {
    #                  'classes': ('collapse',),
    #                  'fields': ('assigned_to', 'assignment_date'),
    #              }),
    #              )


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Item)
admin.site.register(SpecificItem)
admin.site.register(Part)
admin.site.register(ServiceContract)
admin.site.register(Location)
admin.site.register(Vendor)
