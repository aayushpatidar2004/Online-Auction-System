from django.contrib import admin
from .models import WeatherRecord

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'temperature', 'humidity', 'condition', 'rainfall_mm', 'recorded_at')
    list_filter = ('condition', 'state')
    search_fields = ('location_name', 'district')

