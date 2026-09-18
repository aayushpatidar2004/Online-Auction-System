from django.contrib import admin
from .models import FarmerProfile

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'village', 'district', 'state', 'main_crop', 'soil_type')
    search_fields = ('full_name', 'mobile_number', 'village', 'district')
    list_filter = ('state', 'soil_type')

