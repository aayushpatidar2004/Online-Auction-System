from rest_framework import serializers
from .models import Pest

class PestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pest
        fields = '__all__'

