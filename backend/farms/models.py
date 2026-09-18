from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    SOIL_CHOICES = [
        ('Black Soil', 'Black Soil'),
        ('Red Soil', 'Red Soil'),
        ('Alluvial Soil', 'Alluvial Soil'),
        ('Laterite Soil', 'Laterite Soil'),
        ('Sandy Soil', 'Sandy Soil'),
        ('Clay Soil', 'Clay Soil'),
        ('Loamy Soil', 'Loamy Soil'),
    ]

    IRRIGATION_CHOICES = [
        ('Drip Irrigation', 'Drip Irrigation'),
        ('Sprinkler Irrigation', 'Sprinkler Irrigation'),
        ('Canal / Flood Irrigation', 'Canal / Flood Irrigation'),
        ('Borewell / Tube Well', 'Borewell / Tube Well'),
        ('Rainfed (Monsoon Dependent)', 'Rainfed (Monsoon Dependent)'),
    ]

    STATUS_CHOICES = [
        ('Sown', 'Sown / Germinating'),
        ('Vegetative', 'Vegetative Growth'),
        ('Flowering', 'Flowering / Fruiting'),
        ('Maturity', 'Maturity / Ready to Harvest'),
        ('Harvested', 'Harvested'),
        ('Fallow', 'Fallow / Land Preparation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms', null=True, blank=True)
    farm_name = models.CharField(max_length=120)
    village = models.CharField(max_length=100)
    area_acres = models.DecimalField(max_digits=6, decimal_places=2, default=2.5)
    soil_type = models.CharField(max_length=50, choices=SOIL_CHOICES, default='Black Soil')
    current_crop = models.CharField(max_length=100, default='Cotton')
    sowing_date = models.DateField(null=True, blank=True)
    irrigation_type = models.CharField(max_length=50, choices=IRRIGATION_CHOICES, default='Drip Irrigation')
    expected_harvest_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Vegetative')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farm_name} - {self.current_crop} ({self.village})"

