from rest_framework import generics, permissions
from .models import Crop
from .serializers import CropSerializer

class CropListView(generics.ListAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        season = self.request.query_params.get('season')
        search = self.request.query_params.get('search')
        if season:
            qs = qs.filter(season__icontains=season)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

class CropDetailView(generics.RetrieveAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    lookup_field = 'id'

