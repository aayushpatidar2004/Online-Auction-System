from rest_framework import generics, permissions
from .models import Pesticide
from .serializers import PesticideSerializer

class PesticideListView(generics.ListAPIView):
    queryset = Pesticide.objects.all()
    serializer_class = PesticideSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        pest = self.request.query_params.get('pest')
        crop = self.request.query_params.get('crop')
        search = self.request.query_params.get('search')
        if pest:
            qs = qs.filter(target_pests__icontains=pest)
        if crop:
            qs = qs.filter(target_crops__icontains=crop)
        if search:
            qs = qs.filter(product_name__icontains=search) | qs.filter(active_ingredient__icontains=search) | qs.filter(target_pests__icontains=search)
        return qs

class PesticideDetailView(generics.RetrieveAPIView):
    queryset = Pesticide.objects.all()
    serializer_class = PesticideSerializer
    lookup_field = 'id'

