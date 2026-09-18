from django.contrib import admin
from .models import Crop

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'season', 'water_requirement', 'maturity_days')
    list_filter = ('season', 'water_requirement')
    search_fields = ('name', 'scientific_name', 'ideal_soil')
    prepopulated_fields = {'slug': ('name',)}

