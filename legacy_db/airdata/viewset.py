from django.db.models import Count
from viewflow import Icon
from viewflow.urls import (
    Application, DetailViewMixin, DeleteViewMixin,
    ModelViewset, ReadonlyModelViewset
)
from . import models


class AircraftViewset(DetailViewMixin, DeleteViewMixin, ModelViewset):
    icon = Icon('flight')
    model = models.Aircraft
    list_columns = ('code', 'model_name', 'range', 'seats')
    queryset = model._default_manager.annotate(
        seats=Count("seat")
    )

    def seats(self, obj):
        return obj.seats


class AirportViewset(ModelViewset):
    model = models.Airport
    icon = Icon('place')
    list_columns = ('code', 'airport_name', 'city_name', 'timezone')


class BookingViewset(ReadonlyModelViewset):
    model = models.Booking
    icon = Icon('money')
    list_columns = ('ref', 'book_date', 'total_amount')


class TicketViewset(DetailViewMixin, ModelViewset):
    model = models.Ticket
    icon = Icon('style')
    list_columns = ('ticket_no', 'book_ref', 'passenger_name', 'phone')


class FlightViewset(ModelViewset):
    model = models.Flight
    icon = Icon('flight_takeoff')
    list_columns = ('departure_airport', 'scheduled_departure', 'arrival_airport', 'scheduled_arrival', 'status')


class AirportApp(Application):
    icon = Icon('tour')

    items = [
        AircraftViewset(),
        AirportViewset(),
        BookingViewset(),
        TicketViewset(),
        FlightViewset(),
    ]
