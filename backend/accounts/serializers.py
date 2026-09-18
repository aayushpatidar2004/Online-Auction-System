from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FarmerProfile

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'full_name', 'mobile_number', 'village',
            'district', 'state', 'farm_size_acres', 'soil_type',
            'main_crop', 'preferred_language', 'created_at', 'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    farmer_profile = FarmerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'farmer_profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)
    village = serializers.CharField(write_only=True, required=False, default='')
    district = serializers.CharField(write_only=True, required=False, default='')
    state = serializers.CharField(write_only=True, required=False, default='')
    farm_size_acres = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True, required=False, default=2.0)
    soil_type = serializers.CharField(write_only=True, required=False, default='Black Soil')
    main_crop = serializers.CharField(write_only=True, required=False, default='Cotton')
    preferred_language = serializers.CharField(write_only=True, required=False, default='en')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'full_name',
            'mobile_number', 'village', 'district', 'state',
            'farm_size_acres', 'soil_type', 'main_crop', 'preferred_language'
        ]

    def create(self, validated_data):
        profile_data = {
            'full_name': validated_data.pop('full_name'),
            'mobile_number': validated_data.pop('mobile_number'),
            'village': validated_data.pop('village', 'Nagpur'),
            'district': validated_data.pop('district', 'Nagpur'),
            'state': validated_data.pop('state', 'Maharashtra'),
            'farm_size_acres': validated_data.pop('farm_size_acres', 2.0),
            'soil_type': validated_data.pop('soil_type', 'Black Soil'),
            'main_crop': validated_data.pop('main_crop', 'Cotton'),
            'preferred_language': validated_data.pop('preferred_language', 'en'),
        }
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        FarmerProfile.objects.create(user=user, **profile_data)
        return user

