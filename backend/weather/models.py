from django.db import models

class WeatherRecord(models.Model):
    location_name = models.CharField(max_length=150)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage")
    wind_speed = models.FloatField(help_text="Wind speed in km/h")
    condition = models.CharField(max_length=100)
    cloud_percentage = models.IntegerField(default=20)
    rainfall_mm = models.FloatField(default=0.0)
    rain_probability = models.IntegerField(default=10)
    sunrise = models.CharField(max_length=20, default="06:05 AM")
    sunset = models.CharField(max_length=20, default="06:45 PM")
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.location_name} - {self.temperature}°C ({self.condition}) on {self.recorded_at.strftime('%Y-%m-%d')}"

