from django.db.models import Count
from django.contrib import admin
from . import models


class SeatInline(admin.StackedInline):
    model = models.Seat
    extra = 0


@admin.register(models.Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('code', 'model_name', 'range', 'seats')
    fields = ('code', 'en', 'ru', 'range')
    inlines = [SeatInline, ]

    def get_queryset(self, request):
        return (super().get_queryset(request).annotate(
            seats=Count("seat")
        ))

    def seats(self, obj):
        return obj.seats


@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'airport_name', 'city_name', 'timezone')


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('ref', 'book_date', 'total_amount')
    fields = ('ref', 'book_date', 'total_amount')
    readonly_fields = ('ref', )


class TicketFlightInline(admin.StackedInline):
    model = models.TicketFlight
    readonly_fields = ('flight', )
    extra = 0


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_no', 'book_ref', 'passenger_name', 'phone')
    fields = ('book_ref', 'ticket_no', 'passenger_id', 'passenger_name', 'email', 'phone')
    readonly_fields = ('book_ref', )
    inlines = (TicketFlightInline, )


@admin.register(models.Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('departure_airport', 'scheduled_departure', 'arrival_airport', 'scheduled_arrival', 'status')
    list_filter = ('status',)
    date_hierarchy = 'scheduled_departure'
