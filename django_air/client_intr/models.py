from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class AirUser(AbstractUser):
    def __str__(self):
        return self.username


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    country = models.ForeignKey(Country, related_name="cities", on_delete=models.SET_NULL, null=True)


class Airport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, related_name="airports", on_delete=models.CASCADE)


class AirplaneType(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=40)
    base_seats = models.IntegerField()
    premium_seats = models.IntegerField()
    business_seats = models.IntegerField()
    business_rows = models.IntegerField(default=0)
    first_class_rows = models.IntegerField(default=0)
    economy_rows = models.IntegerField(default=0)
    seats_per_business_row = models.IntegerField(default=4)
    seats_per_first_class_row = models.IntegerField(default=2)
    seats_per_economy_row = models.IntegerField(default=6)

    def str(self):
        return self.model_name


class Airplane(models.Model):
    id = models.AutoField(primary_key=True)
    airplane_type = models.ForeignKey(AirplaneType, related_name="airplanes", on_delete=models.CASCADE)


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)


class BaggageSize(models.Model):
    id = models.AutoField(primary_key=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    max_weight = models.IntegerField(default=0)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = CharField(max_length=30, default="")
    meal = models.ForeignKey(Meal, related_name="services", null=True, on_delete=models.SET_NULL)
    baggage = models.ForeignKey(BaggageSize, related_name="services", null=True, on_delete=models.SET_NULL)


class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    origin_airport = models.ForeignKey(Airport, related_name="origin_flights", on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name="arrival_flights", on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name="destination_flights", on_delete=models.CASCADE,
                                    db_index=True)
    origin = models.ForeignKey(City, related_name="origin_flights", on_delete=models.CASCADE,
                               db_index=True)
    airplane = models.ForeignKey(Airplane, related_name="flights", on_delete=models.CASCADE)
    available_services = models.ManyToManyField(
        Service,
        through='ServiceOffer',
        related_name='offered_on_flights'
    )
    date_of_flight = models.DateTimeField()
    arriving_date = models.DateTimeField()
    base_seat_price = models.IntegerField(default=0)
    first_class_seat_price = models.IntegerField(default=0)
    business_seat_price = models.IntegerField(default=0)


class ServiceOffer(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Passenger(models.Model):
    GENDER_CHOICE = [
        ("F", "Female"),
        ("M", "Male"),
        ("U", "Undisclosed"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default="U")


class Seat(models.Model):
    CLASS_CHOICE = [
        ("EC", "Economy"),
        ("BC", "Business"),
        ("FC", "First class")
    ]
    id = models.AutoField(primary_key=True)
    flight_class = models.CharField(max_length=2, choices=CLASS_CHOICE)
    flight_id = models.ForeignKey(Flight, related_name="seats", on_delete=models.CASCADE)
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)


class Order(models.Model):
    payment = models.FloatField(default=0)
    id = models.AutoField(primary_key=True)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    seat_id = models.OneToOneField(Seat, related_name="ticket", null=True, on_delete=models.SET_NULL)
    passenger_id = models.ForeignKey(Passenger, related_name="seats", null=True, on_delete=models.SET_NULL)
    order_id = models.ForeignKey(Order, related_name="tickets", null=True, on_delete=models.SET_NULL)
    services = models.ForeignKey(Service, related_name="tickets", null=True, on_delete=models.SET_NULL)
