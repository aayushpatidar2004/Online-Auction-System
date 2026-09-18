from rest_framework import serializers
from .models import SoilRecord

class SoilRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilRecord
        fields = '__all__'

class SoilAnalysisInputSerializer(serializers.Serializer):
    soil_type = serializers.ChoiceField(choices=SoilRecord.SOIL_TYPES, default='Black Soil')
    ph = serializers.FloatField(min_value=3.0, max_value=11.0, default=6.8)
    nitrogen = serializers.FloatField(min_value=0.0, max_value=1000.0, default=320.0)
    phosphorus = serializers.FloatField(min_value=0.0, max_value=200.0, default=18.0)
    potassium = serializers.FloatField(min_value=0.0, max_value=800.0, default=210.0)
    moisture = serializers.FloatField(min_value=0.0, max_value=100.0, default=52.0)
    organic_carbon = serializers.FloatField(min_value=0.0, max_value=10.0, default=0.65)

