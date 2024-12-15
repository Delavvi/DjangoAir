from django.contrib import admin
from django.urls import path
from .views import FlightsList, FlightDetailView, CitiesListView

urlpatterns = [
    path('flights', FlightsList.as_view(), name="flights_list"),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('cities', CitiesListView.as_view(), name='cities_list'),
]
