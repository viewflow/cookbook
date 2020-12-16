from django.db import connections
from django.test import TestCase
from cookbook.legacy_db.airdata.models import Aircraft, Seat


class Test(TestCase):
    databases = ['default', 'demo']

    @classmethod
    def setUpTestData(cls):
        with connections['demo'].cursor() as cursor:
            cursor.execute("""
CREATE TABLE aircrafts_data (
    aircraft_code character(3) NOT NULL,
    model jsonb NOT NULL,
    range integer NOT NULL,
    CONSTRAINT aircrafts_range_check CHECK ((range > 0))
);

CREATE TABLE seats (
    aircraft_code character(3) NOT NULL,
    seat_no character varying(4) NOT NULL,
    fare_conditions character varying(10) NOT NULL,
    CONSTRAINT seats_fare_conditions_check CHECK (
        ((fare_conditions)::text = ANY (ARRAY[
            ('Economy'::character varying)::text, ('Comfort'::character varying)::text,
            ('Business'::character varying)::text]))
    )
);

ALTER TABLE ONLY aircrafts_data
    ADD CONSTRAINT aircrafts_pkey PRIMARY KEY (aircraft_code);

ALTER TABLE ONLY seats
    ADD CONSTRAINT seats_pkey PRIMARY KEY (aircraft_code, seat_no);

ALTER TABLE ONLY seats
    ADD CONSTRAINT seats_aircraft_code_fkey FOREIGN KEY (aircraft_code) REFERENCES aircrafts_data(aircraft_code)
    ON DELETE CASCADE;
""")

    def setUp(self):
        self.craft = Aircraft.objects.create(code='TST', model={'ru': 'Test', 'en': 'Test'}, range=1)
        self.seat1a = Seat.objects.create(aircraft_code=self.craft, seat_no='1A', fare_conditions='Business')
        self.seat1b = Seat.objects.create(aircraft_code=self.craft, seat_no='1B', fare_conditions='Business')

    def test_count_query(self):
        self.assertEqual(Aircraft.objects.all().count(), 1)
        self.assertEqual(Seat.objects.all().count(), 2)

    def test_related_access(self):
        self.assertEqual(self.craft.seat_set.count(), 2)

    def test_save(self):
        self.seat1a.save()
