from django.contrib import admin
from .models import SoilRecord

@admin.register(SoilRecord)
class SoilRecordAdmin(admin.ModelAdmin):
    list_display = ('soil_type', 'ph', 'health_score', 'health_status', 'created_at')
    list_filter = ('soil_type', 'health_status')

