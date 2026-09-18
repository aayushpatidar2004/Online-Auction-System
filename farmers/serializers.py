from rest_framework import serializers
from .models import Farmer, Crop

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'user', 'phone', 'address']
        read_only_fields = ['id']

class CropSerializer(serializers.ModelSerializer):
    farmer = serializers.PrimaryKeyRelatedField(queryset=Farmer.objects.all())

    class Meta:
        model = Crop
        fields = ['id', 'farmer', 'name', 'quantity_kg', 'price_per_kg', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
