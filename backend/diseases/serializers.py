from rest_framework import serializers
from .models import Disease, PlantAnalysis

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class PlantAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantAnalysis
        fields = '__all__'

