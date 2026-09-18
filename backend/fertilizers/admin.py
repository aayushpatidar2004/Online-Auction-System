from django.contrib import admin
from .models import Fertilizer

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'nutrient_composition', 'suitable_soil')
    list_filter = ('category',)
    search_fields = ('name', 'nutrient_composition', 'suitable_crops')
