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
class LegSerializer(serializers.Serializer):
    name = serializers.CharField()
    miles = serializers.FloatField()
    hours = serializers.FloatField()
    endsWith = serializers.CharField()


class PlanRouteSerializer(serializers.Serializer):
    distanceMiles = serializers.FloatField()
    drivingHours = serializers.FloatField()
    legs = LegSerializer(many=True)


class LegSerializer(serializers.Serializer):
    name = serializers.CharField()
    miles = serializers.FloatField()
    hours = serializers.FloatField()
    endsWith = serializers.CharField()


class PlanRouteSerializer(serializers.Serializer):
    distanceMiles = serializers.FloatField()
    drivingHours = serializers.FloatField()
    legs = LegSerializer(many=True)


class HOSRulesSerializer(serializers.Serializer):
    maxDrivingHours = serializers.FloatField()
    maxDutyWindowHours = serializers.FloatField()
    requiredRestHours = serializers.FloatField()
    breakAfterDrivingHours = serializers.FloatField()
    requiredBreakHours = serializers.FloatField()
    maxCycleHours = serializers.FloatField()
    restartHours = serializers.FloatField()
    fuelIntervalMiles = serializers.FloatField()
    fuelStopHours = serializers.FloatField()
    pickupHours = serializers.FloatField()
    dropoffHours = serializers.FloatField()
    startHour = serializers.FloatField()


class PlanTripSerializer(serializers.Serializer):
    route = PlanRouteSerializer()
    cycleUsed = serializers.FloatField()
    rules = HOSRulesSerializer()