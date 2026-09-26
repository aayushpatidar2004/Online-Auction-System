from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password', 'password2')

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with that username already exists.')
        return value

    def validate_email(self, value):
        if value and CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return value

    def validate_phone(self, value):
        if value and CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError('A user with that phone number already exists.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'seller_rating',
                  'buyer_rating', 'wallet_balance', 'profile_image', 'created_at',
                  'is_staff', 'is_superuser')
        read_only_fields = ('id', 'username', 'seller_rating', 'buyer_rating', 'created_at', 'is_staff', 'is_superuser')
