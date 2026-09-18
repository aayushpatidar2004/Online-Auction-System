from rest_framework import serializers
from .models import Fertilizer

class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'
