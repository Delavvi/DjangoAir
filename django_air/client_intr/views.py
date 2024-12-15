from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Flight, City, Service, ServiceOffer
from .serializers import FlightSerializer, FlightDetailSerializer, CitySerializer


class FlightPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'flights_num'
    max_page_size = 20


class FlightsList(ListAPIView):
    serializer_class = FlightSerializer
    pagination_class = FlightPagination

    def get_queryset(self):
        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        min_departure_date_str = self.request.query_params.get('date')

        if origin and destination and min_departure_date_str:
            min_date = None
            try:
                min_date = datetime.strptime(min_departure_date_str, '%Y-%m-%d')
            except ValueError:
                try:
                    min_date = datetime.strptime(min_departure_date_str, '%d.%m.%Y')
                    min_date = min_date.strftime('%d.%m.%Y')
                except ValueError:
                    return Response({"error": "Invalid date format. Use YYYY-MM-DD or DD.MM.YYYY."},
                                    status=HTTP_400_BAD_REQUEST)
            start_of_day = min_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = min_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            flights = Flight.objects.filter(
                destination__name__icontains=destination,
                origin__name__icontains=origin,
                date_of_flight__range=(start_of_day, end_of_day)
            ).order_by("name")
        else:
            flights = Flight.objects.all().select_related("destination", "origin").order_by("destination")
        return flights


class FlightDetailView(RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightDetailSerializer

    def get_object(self):
        id = self.kwargs.get("pk")
        flight_object = get_object_or_404(
            Flight.objects.select_related(
                "origin",
                "destination",
                "origin_airport",
                "destination_airport"
            ).prefetch_related(
                Prefetch(
                    'available_services',
                    queryset=Service.objects.prefetch_related(
                        Prefetch(
                            'serviceoffer_set',
                            queryset=ServiceOffer.objects.filter(flight__id=id).prefetch_related("service")
                        )
                    ),
                    to_attr='prefetched_services'
                )
            ),
            id=id
        )
        return flight_object


class CitiesListView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            cities = City.objects.filter(name__icontains=name)[:5]
        else:
            cities = City.objects.none()
        return cities
