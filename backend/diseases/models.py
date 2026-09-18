from django.db import models
from django.contrib.auth.models import User

class Disease(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low Severity'),
        ('Moderate', 'Moderate Severity'),
        ('High', 'High Severity / Epidemic Risk'),
    ]

    disease_name = models.CharField(max_length=150, unique=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    crop = models.CharField(max_length=100, default='Tomato')
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='Moderate')
    symptoms = models.TextField()
    possible_causes = models.TextField()
    organic_management = models.TextField()
    chemical_management = models.TextField()
    prevention = models.TextField()
    when_to_consult_expert = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['disease_name']

    def __str__(self):
        return f"{self.disease_name} ({self.crop})"

class PlantAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='plant_analyses')
    image = models.ImageField(upload_to='plant_scans/%Y/%m/%d/')
    plant_name = models.CharField(max_length=100, default='Plant')
    detected_condition = models.CharField(max_length=150)
    confidence = models.FloatField(default=0.0)
    severity = models.CharField(max_length=50, default='Moderate')
    is_healthy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.plant_name}: {self.detected_condition} ({self.confidence}%)"

