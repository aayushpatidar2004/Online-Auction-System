from django.contrib import admin
from .models import Disease, PlantAnalysis

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'crop', 'scientific_name', 'severity')
    list_filter = ('severity', 'crop')
    search_fields = ('disease_name', 'crop', 'symptoms')

@admin.register(PlantAnalysis)
class PlantAnalysisAdmin(admin.ModelAdmin):
    list_display = ('plant_name', 'detected_condition', 'confidence', 'severity', 'is_healthy', 'created_at')
    list_filter = ('is_healthy', 'severity')

