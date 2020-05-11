from rest_framework import serializers

from .models import FactDeliveryTime


class DeliveryTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactDeliveryTime
        fields = "__all__"
