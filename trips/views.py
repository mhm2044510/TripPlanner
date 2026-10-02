from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TripSerializer,GeocodeSerializer,RouteSerializer
from .services import geocode,get_route
from .models import City
class TripsView(APIView):
    def get(self,request):
        return Response({
            "message":"Trips API is working"
        })
    def post(self,request):
        serialzar=TripSerializer(data=request.data)
        if serialzar.is_valid():
         return Response({
            "received_data":request.data
            })
        return Response(serialzar.errors,status=400 )
           
class GeocodeView(APIView):

     def post(self, request):

        serializer = GeocodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        data = serializer.validated_data

        pickup =  geocode(data["pickup"])
        dropoff =  geocode(data["dropoff"])
        current_location =  geocode(data["current_location"])
        return Response({
            "pickup": pickup,
            "dropoff": dropoff,
            "current_location": current_location
        }) 
class RouteView(APIView):

     def post(self, request):
        serializer = RouteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        try:
            route =  get_route(
                data["current"],
                data["pickup"],
                data["dropoff"]
            )

            return Response(route)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=400
            )
class CitiesView(APIView):

    def get(self, request):
        cities = City.objects.all()

        return Response([
            city.name
            for city in cities
        ])                   
# Create your views here.
