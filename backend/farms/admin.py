from django.contrib import admin
from .models import Farm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'village', 'area_acres', 'soil_type', 'current_crop', 'stage')
    list_filter = ('soil_type', 'stage')
    search_fields = ('farm_name', 'village', 'current_crop')

