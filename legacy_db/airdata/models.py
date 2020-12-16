from django.db import models
from django.utils import translation
from viewflow import jsonstore
from viewflow.fields import CompositeKey


class Aircraft(models.Model):
    code = models.CharField(
        db_column='aircraft_code',
        help_text='Aircraft code, IATA',
        max_length=3,
        primary_key=True,
    )
    model = models.JSONField(help_text='Aircraft model')
    range = models.IntegerField(help_text='Maximal flying distance, km')

    en = jsonstore.CharField(json_field_name='model', max_length=250)
    ru = jsonstore.CharField(json_field_name='model', max_length=250)

    @property
    def model_name(self):
        if self.model:
            if translation.get_language() == 'ru':
                return self.model.get('ru')
            return self.model.get('en')

    def __str__(self):
        return self.model_name or ''

    class Meta:
        managed = False
        db_table = 'aircrafts_data'


class Seat(models.Model):
    id = CompositeKey(columns=['aircraft_code', 'seat_no'])
    aircraft_code = models.ForeignKey(Aircraft, models.DO_NOTHING, db_column='aircraft_code')
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_no or ''

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('aircraft_code', 'seat_no'),)


class Airport(models.Model):
    code = models.CharField(
        db_column='airport_code',
        max_length=3,
        primary_key=True,
    )
    name = models.JSONField(db_column='airport_name')
    city = models.JSONField()
    coordinates = models.CharField(max_length=250)
    timezone = models.TextField()

    def airport_name(self):
        if self.name:
            return self.name.get(
                'ru' if translation.get_language() == 'ru' else 'en'
            )

    def city_name(self):
        if self.city:
            return self.city.get(
                'ru' if translation.get_language() == 'ru' else 'en'
            )

    def __str__(self):
        return self.code

    class Meta:
        managed = False
        db_table = 'airports_data'


class BoardingPass(models.Model):
    id = CompositeKey(columns=['boarding_no', 'flight_id'])
    ticket_no = models.ForeignKey('TicketFlight', models.DO_NOTHING, db_column='ticket_no')
    flight_id = models.IntegerField()
    boarding_no = models.IntegerField(help_text='Boarding pass number')
    seat_no = models.CharField(max_length=4, help_text='Seat number')

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        unique_together = (('flight_id', 'boarding_no'), ('flight_id', 'seat_no'), ('ticket_no', 'flight_id'),)


class Booking(models.Model):
    ref = models.CharField(primary_key=True, max_length=6, db_column='book_ref')
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ref

    class Meta:
        managed = False
        db_table = 'bookings'


class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(
        Airport,
        models.DO_NOTHING,
        db_column='departure_airport',
        related_name='+',
    )
    arrival_airport = models.ForeignKey(
        Airport,
        models.DO_NOTHING,
        db_column='arrival_airport',
        related_name='+',
    )
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey(Aircraft, models.DO_NOTHING, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.departure_airport} -> {self.arrival_airport}"

    class Meta:
        managed = False
        db_table = 'flights'
        unique_together = (('flight_no', 'scheduled_departure'),)


class TicketFlight(models.Model):
    id = CompositeKey(columns=['ticket_no', 'flight'])
    ticket_no = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticket_no')
    flight = models.ForeignKey(Flight, models.DO_NOTHING)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ticket_no}: {self.flight}"

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        unique_together = (('ticket_no', 'flight'),)


class Ticket(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey(Booking, models.DO_NOTHING, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = models.JSONField(blank=True, null=True)
    flights = models.ManyToManyField(Flight, through=TicketFlight, related_name='tickets')

    email = jsonstore.CharField(json_field_name='contact_data', max_length=250)
    phone = jsonstore.CharField(json_field_name='contact_data', max_length=250)

    def __str__(self):
        return f"{self.ticket_no}"

    class Meta:
        managed = False
        db_table = 'tickets'
