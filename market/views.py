from rest_framework import viewsets, permissions
from .models import PriceData
from .serializers import PriceDataSerializer

class PriceDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceData.objects.all()
    serializer_class = PriceDataSerializer
    permission_classes = [permissions.AllowAny]

