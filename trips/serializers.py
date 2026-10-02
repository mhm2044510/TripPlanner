from rest_framework import serializers
class TripSerializer(serializers.Serializer):
    origin = serializers.CharField()
    destination = serializers.CharField()

class GeocodeSerializer(serializers.Serializer):

    pickup = serializers.CharField()
    dropoff = serializers.CharField()
    current_location = serializers.CharField()
    
class RouteSerializer(serializers.Serializer):
    current = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )

    pickup = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )

    dropoff = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2
    )    
