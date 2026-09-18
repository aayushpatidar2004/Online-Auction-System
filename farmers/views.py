from rest_framework import viewsets, permissions
from .models import Farmer, Crop
from .serializers import FarmerSerializer, CropSerializer

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.select_related('farmer').all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
