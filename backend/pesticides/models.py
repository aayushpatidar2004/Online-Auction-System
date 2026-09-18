from django.db import models

class Pesticide(models.Model):
    TOXICITY_CHOICES = [
        ('Green', 'Slightly Toxic (Green Label)'),
        ('Blue', 'Moderately Toxic (Blue Label)'),
        ('Yellow', 'Highly Toxic (Yellow Label)'),
        ('Red', 'Extremely Toxic (Red Label)'),
        ('Bio', 'Bio-Pesticide / Organic (Botanical/Microbial)'),
    ]

    product_name = models.CharField(max_length=150)
    active_ingredient = models.CharField(max_length=150)
    chemical_class = models.CharField(max_length=100, default='Insecticide / Fungicide')
    toxicity_label = models.CharField(max_length=20, choices=TOXICITY_CHOICES, default='Green')
    target_pests = models.CharField(max_length=255, help_text="Target pests / diseases")
    target_crops = models.CharField(max_length=255, help_text="Approved crops")
    mode_of_action = models.TextField(help_text="Systemic, Contact, Stomach action, etc.")
    general_usage_info = models.TextField(help_text="General timing and method")
    safety_precautions = models.TextField(help_text="Crucial handling and sprayer safety")
    ppe_requirements = models.TextField(help_text="Gloves, mask, goggles, boots, apron")
    pre_harvest_interval_days = models.IntegerField(default=7, help_text="Days to wait before harvest")
    storage_guidelines = models.TextField(help_text="Safe locked storage instructions")
    environmental_precautions = models.TextField(help_text="Protection of bees, aquatic life, groundwater")
    disclaimer = models.TextField(
        default="Always follow the product label, local agricultural authority guidance, and advice from a qualified agriculture professional before application."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product_name']

    def __str__(self):
        return f"{self.product_name} ({self.active_ingredient})"

