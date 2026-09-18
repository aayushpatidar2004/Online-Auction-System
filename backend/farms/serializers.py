from rest_framework import serializers
from .models import Farm

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            'id', 'farm_name', 'village', 'area_acres', 'soil_type',
            'current_crop', 'sowing_date', 'irrigation_type',
            'expected_harvest_date', 'stage', 'notes', 'created_at', 'updated_at'
        ]

