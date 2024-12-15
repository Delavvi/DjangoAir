from rest_framework import serializers
from .models import Flight, Airport, City, Airplane, Service, Country, AirplaneType, ServiceOffer, Meal, BaggageSize


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "airplane_type"]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        airplane_type = AirplaneTypeSerializer()
        fields = ['id', 'airplane_type']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "name"]


class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaggageSize
        fields = ["id", "width", "height", "max_weight"]


class ServiceSerializer(serializers.ModelSerializer):
    meal = MealSerializer()
    baggage = BaggageSerializer()
    class Meta:
        model = Service
        fields = ['id', 'meal', 'baggage', 'name']


class ServiceOfferSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = ServiceOffer
        fields = ['service', 'price']


class FlightSerializer(serializers.ModelSerializer):
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    origin = CitySerializer()
    destination = CitySerializer()

    class Meta:
        model = Flight
        fields = [
            'id',
            'origin_airport',
            'destination_airport',
            'origin',
            'destination',
            'date_of_flight',
            'arriving_date'
        ]


class FlightDetailSerializer(serializers.ModelSerializer):
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()
    origin = CitySerializer()
    destination = CitySerializer()
    airplane = AirplaneSerializer()
    available_services = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = [
            'id',
            'origin_airport',
            'destination_airport',
            'origin',
            'destination',
            'airplane',
            'available_services',
            'date_of_flight',
            'arriving_date'
        ]

    def get_available_services(self, obj):
        services = ServiceOffer.objects.filter(flight=obj)
        return ServiceOfferSerializer(services, many=True).data
