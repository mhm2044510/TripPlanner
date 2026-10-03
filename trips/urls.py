from django.urls import path
from .views import TripsView,GeocodeView,RouteView,CitiesView,PlanTripView
urlpatterns = [
    path('', TripsView.as_view()),
    path('GetGeoCode/',GeocodeView.as_view()),
    path('GetRoute/', RouteView.as_view()),
    path('cities/', CitiesView.as_view()),
    path('PlanTrip/', PlanTripView.as_view()),
]