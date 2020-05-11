from datetime import datetime

from rest_framework.viewsets import ModelViewSet
import luigi

from .models import FactDeliveryTime, DimQueryTime
from .serializers import DeliveryTimeSerializer
from grocer.instacart.tasks import GetDeliveryTimes


class DeliveryTime(ModelViewSet):
    def get_queryset(self):

        queryset = FactDeliveryTime.objects.filter(
            timestamp=FactDeliveryTime.objects.latest("timestamp")
        ).values()
        return queryset

    serializer_class = DeliveryTimeSerializer
