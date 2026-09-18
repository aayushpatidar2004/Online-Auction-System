from django.db import models

class Pest(models.Model):
    pest_name = models.CharField(max_length=150, unique=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    affected_crops = models.CharField(max_length=255, help_text="Comma-separated crops")
    identification = models.TextField(help_text="Visual characteristics of the insect")
    symptoms = models.TextField(help_text="Field damage symptoms")
    life_cycle = models.TextField(help_text="Egg, nymph/larvae, pupa, adult stages")
    prevention = models.TextField(help_text="Cultural and preventive measures")
    organic_control = models.TextField(help_text="Bio-pesticides, neem extracts, traps")
    biological_control = models.TextField(help_text="Natural predators and parasitoids")
    chemical_control = models.TextField(help_text="Recommended chemical classes with disclaimer")
    safety_precautions = models.TextField(help_text="Protective measures and spray timing")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pest_name']

    def __str__(self):
        return self.pest_name

