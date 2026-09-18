from django.db import models
from django.contrib.auth.models import User

class SoilRecord(models.Model):
    SOIL_TYPES = [
        ('Black Soil', 'Black Soil'),
        ('Red Soil', 'Red Soil'),
        ('Alluvial Soil', 'Alluvial Soil'),
        ('Laterite Soil', 'Laterite Soil'),
        ('Sandy Soil', 'Sandy Soil'),
        ('Clay Soil', 'Clay Soil'),
        ('Loamy Soil', 'Loamy Soil'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='soil_records')
    soil_type = models.CharField(max_length=50, choices=SOIL_TYPES, default='Black Soil')
    ph = models.FloatField(help_text="pH value (0-14)")
    nitrogen = models.FloatField(help_text="Nitrogen (kg/ha or mg/kg)")
    phosphorus = models.FloatField(help_text="Phosphorus (kg/ha)")
    potassium = models.FloatField(help_text="Potassium (kg/ha)")
    moisture = models.FloatField(help_text="Moisture percentage (0-100)")
    organic_carbon = models.FloatField(help_text="Organic Carbon percentage", default=0.6)
    health_score = models.IntegerField(default=75, help_text="Calculated health score 0-100")
    health_status = models.CharField(max_length=50, default="Healthy")
    suitable_crops = models.CharField(max_length=255, default="Cotton, Soybean, Wheat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.soil_type} (pH {self.ph}) - {self.health_status} on {self.created_at.strftime('%Y-%m-%d')}"

