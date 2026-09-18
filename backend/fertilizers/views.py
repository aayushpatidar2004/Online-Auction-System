from rest_framework import generics, permissions
from .models import Fertilizer
from .serializers import FertilizerSerializer

class FertilizerListView(generics.ListAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category__icontains=category)
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(nutrient_composition__icontains=search)
        return qs

class FertilizerDetailView(generics.RetrieveAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
    lookup_field = 'id'

