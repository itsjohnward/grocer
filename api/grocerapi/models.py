from django.db import models


class DimQueryTime(models.Model):
    timestamp = models.DateTimeField("timestamp")

    def __str__(self):
        return self.timestamp


class FactDeliveryTime(models.Model):
    timestamp = models.ForeignKey(DimQueryTime, on_delete=models.CASCADE)
    slot_start = models.DateTimeField("slot_start", null=True)  # Allow NULL
    slot_end = models.DateTimeField("slot_end", null=True)  # Allow NULL
    price = models.FloatField("price", null=True)

    def __str__(self):
        return "{}: {} - {} (${})".format(
            str(self.timestamp), str(self.slot_start), str(self.slot_end), self.price
        )
