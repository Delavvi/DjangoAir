from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flight, Seat, AirplaneType


@receiver(post_save, sender=Flight)
def post_save_flight(sender, instance: Flight, created, **kwargs):
    if created:
        airplane_type: AirplaneType = instance.airplane.airplane_type

        row_number = 1

        for row in range(airplane_type.first_class_rows):
            for seat in range(airplane_type.seats_per_first_class_row):
                Seat.objects.create(
                    flight_class='FC',
                    row=1,
                    column=seat,
                    flight_id=instance
                )
            row_number += 1

        for row in range(airplane_type.business_rows):
            for seat in range(airplane_type.seats_per_business_row):
                Seat.objects.create(
                    flight_class='BC',
                    row=1,
                    column=seat,
                    flight_id=instance
                )
            row_number += 1

        for row in range(airplane_type.economy_rows):
            for seat in range(airplane_type.seats_per_economy_row):
                letter = chr(ord('A') + seat)
                Seat.objects.create(
                    flight_class='EC',
                    row=1,
                    column=seat,
                    flight_id=instance
                )
            row_number += 1
