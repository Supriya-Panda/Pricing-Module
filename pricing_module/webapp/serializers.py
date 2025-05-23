from rest_framework import serializers

DAY_CHOICES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

class PriceCalculationSerializer(serializers.Serializer):
    distance_km = serializers.FloatField(min_value=0)
    total_minutes = serializers.IntegerField(min_value=0)
    waiting_minutes = serializers.IntegerField(min_value=0)
    day_of_week = serializers.ChoiceField(choices=DAY_CHOICES)
