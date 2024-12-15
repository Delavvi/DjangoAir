from faker import Faker
from django.db import transaction
from django.core.management.base import BaseCommand
from ...models import City, AirplaneType, Airport, Flight, Airplane, Meal, Service, BaggageSize, Country, ServiceOffer
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Fill database with fake data'

    def handle(self, *args, **options):
        fake = Faker()
        fake.seed_instance(42)
        airplane_type = AirplaneType.objects.create(model_name='B1', base_seats=20, premium_seats=20, business_seats=20,
                                                    business_rows=4, economy_rows=4, first_class_rows=4,
                                                    seats_per_business_row=5, seats_per_first_class_row=5,
                                                    seats_per_economy_row=5)
        airplane = Airplane.objects.create(airplane_type=airplane_type)
        for city in range(20):
            with transaction.atomic():
                city_name1 = fake.city()
                city_name2 = fake.city()
                country1 = Country.objects.create(name=fake.country())
                country2 = Country.objects.create(name=fake.country())
                city_object1 = City.objects.create(country=country1, name=city_name1)
                city_object2 = City.objects.create(country=country2, name=city_name2)
                airport1 = Airport.objects.create(name=f"{city_name1}_airport", city=city_object1)
                airport2 = Airport.objects.create(name=f"{city_name2}_airport", city=city_object2)
                timezone = pytz.UTC
                date_of_flight = datetime.strptime('10.10.2027 14:30', '%d.%m.%Y %H:%M').replace(tzinfo=timezone)
                arriving_date = datetime.strptime('10.10.2027 17:30', '%d.%m.%Y %H:%M').replace(tzinfo=timezone)
                meal1 = Meal.objects.create(name="Pizza")
                meal2 = Meal.objects.create(name="Sandwich")
                baggage_size1 = BaggageSize.objects.create(width=30, height=20, max_weight=5)
                baggage_size2 = BaggageSize.objects.create(width=50, height=25, max_weight=10)
                service1 = Service.objects.create(name="Basic", meal=meal1, baggage=baggage_size1)
                service2 = Service.objects.create(name="Comfort", meal=meal2, baggage=baggage_size2)
                flight = Flight.objects.create(
                    origin_airport=airport1,
                    destination_airport=airport2,
                    destination=city_object1,
                    origin=city_object2,
                    airplane=airplane,
                    date_of_flight=date_of_flight,
                    arriving_date=arriving_date,
                )
                service_offer = ServiceOffer.objects.create(service=service1, flight=flight, price=fake.pyint(20, 110))
                service_offer1 = ServiceOffer.objects.create(service=service2, flight=flight, price=fake.pyint(20, 110))
