from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    SOIL_CHOICES = [
        ('Black Soil', 'Black Soil'),
        ('Red Soil', 'Red Soil'),
        ('Alluvial Soil', 'Alluvial Soil'),
        ('Laterite Soil', 'Laterite Soil'),
        ('Sandy Soil', 'Sandy Soil'),
        ('Clay Soil', 'Clay Soil'),
        ('Loamy Soil', 'Loamy Soil'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi (हिंदी)'),
        ('te', 'Telugu (తెలుగు)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15, unique=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    farm_size_acres = models.DecimalField(max_digits=6, decimal_places=2, default=2.0)
    soil_type = models.CharField(max_length=50, choices=SOIL_CHOICES, default='Black Soil')
    main_crop = models.CharField(max_length=100, default='Cotton')
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.village}, {self.district})"

