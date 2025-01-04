from django.contrib import admin
from core.models import Location, Event, EventImages, Cart, Ticket

class EventImageAdmin(admin.TabularInline):
    model = EventImages

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageAdmin]
    list_display = ['title', 'event_image', 'price', 'location', 'available_tickets']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['lid', 'location']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'quantity']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'quantity', 'purchase_date', 'total_price']

admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Ticket, TicketAdmin)
