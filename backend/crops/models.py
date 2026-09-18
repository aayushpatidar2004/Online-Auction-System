from django.db import models

class Crop(models.Model):
    SEASON_CHOICES = [
        ('Kharif', 'Kharif (Monsoon)'),
        ('Rabi', 'Rabi (Winter)'),
        ('Zaid', 'Zaid (Summer)'),
        ('All Seasons', 'All Seasons / Perennial'),
    ]

    WATER_CHOICES = [
        ('Low', 'Low (300-500 mm)'),
        ('Moderate', 'Moderate (500-800 mm)'),
        ('High', 'High (800-1400 mm)'),
        ('Very High', 'Very High (>1400 mm)'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    season = models.CharField(max_length=50, choices=SEASON_CHOICES, default='Kharif')
    water_requirement = models.CharField(max_length=50, choices=WATER_CHOICES, default='Moderate')
    ideal_soil = models.CharField(max_length=150, default='Alluvial Soil, Loamy Soil')
    optimal_temp_range = models.CharField(max_length=50, default='20°C - 30°C')
    optimal_rainfall_range = models.CharField(max_length=50, default='600 - 1000 mm')
    optimal_ph_range = models.CharField(max_length=50, default='6.0 - 7.5')
    maturity_days = models.IntegerField(default=120, help_text="Duration from sowing to harvest")
    description = models.TextField()
    sowing_window = models.CharField(max_length=100, default='June - July')
    harvest_window = models.CharField(max_length=100, default='October - November')
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.season})"

