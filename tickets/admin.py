from django.contrib import admin

# Register your models here.
from tickets.models import *


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'description', 'assigned_to')
    list_filter = ('assigned', 'created_at')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Item)
admin.site.register(SpecificItem)
admin.site.register(Part)
admin.site.register(ServiceContract)
admin.site.register(Location)
admin.site.register(Vendor)
