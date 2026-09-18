from django.db import models

class Fertilizer(models.Model):
    CATEGORY_CHOICES = [
        ('Chemical Nitrogenous', 'Chemical Nitrogenous (e.g. Urea)'),
        ('Chemical Phosphatic', 'Chemical Phosphatic (e.g. DAP, SSP)'),
        ('Chemical Potassic', 'Chemical Potassic (e.g. MOP)'),
        ('Complex NPK', 'Complex NPK Fertilizers'),
        ('Organic & Bio', 'Organic & Bio-Fertilizers (Vermicompost, FYM)'),
        ('Micronutrients', 'Micronutrients (Zinc, Boron, Iron, Manganese)'),
    ]

    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Chemical Nitrogenous')
    nutrient_composition = models.CharField(max_length=255, help_text="e.g. 46% N, 18-46-0 NPK, etc.")
    suitable_soil = models.CharField(max_length=255, default='All soil types')
    suitable_crops = models.CharField(max_length=255, default='Cereals, Pulses, Oilseeds, Cash Crops')
    general_information = models.TextField(help_text="Detailed agronomic purpose and roles")
    application_method = models.TextField(help_text="Basal, top dressing, foliar spray, fertigation")
    safety_environmental = models.TextField(help_text="Preventing leaching, groundwater contamination, split application")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category})"

