from django.contrib import admin

# Register your models here.
from tickets.models import *


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'title', 'creator', 'assigned_to', 'created_at', 'time_open')
    list_filter = ('status', 'assigned', 'created_at')
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
