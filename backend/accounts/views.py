from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import FarmerProfile
from .serializers import RegisterSerializer, UserSerializer, FarmerProfileSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        profile = getattr(self.user, 'farmer_profile', None)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'full_name': profile.full_name if profile else self.user.username,
            'mobile_number': profile.mobile_number if profile else '',
            'village': profile.village if profile else '',
            'district': profile.district if profile else '',
            'state': profile.state if profile else '',
            'soil_type': profile.soil_type if profile else 'Black Soil',
            'main_crop': profile.main_crop if profile else 'Cotton',
            'preferred_language': profile.preferred_language if profile else 'en'
        }
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = user.farmer_profile
        return Response({
            'message': 'Farmer registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': profile.full_name,
                'mobile_number': profile.mobile_number,
                'village': profile.village,
                'district': profile.district,
                'state': profile.state,
                'soil_type': profile.soil_type,
                'main_crop': profile.main_crop,
                'preferred_language': profile.preferred_language
            }
        }, status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = FarmerProfile.objects.get_or_create(user=request.user)
        serializer = FarmerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'profile': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

