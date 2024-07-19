from django.db import models

# Create your models here.
class SensorData(models.Model):
    waterLevel = models.FloatField()
    rainfall = models.FloatField()
    pHValue = models.FloatField()
    soilMoisture = models.FloatField()
    flowRate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SensorData at {self.timestamp}"
