from rest_framework import generics, permissions
from .models import Pest
from .serializers import PestSerializer

class PestListView(generics.ListAPIView):
    queryset = Pest.objects.all()
    serializer_class = PestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        crop = self.request.query_params.get('crop')
        search = self.request.query_params.get('search')
        if crop:
            qs = qs.filter(affected_crops__icontains=crop)
        if search:
            qs = qs.filter(pest_name__icontains=search) | qs.filter(affected_crops__icontains=search)
        return qs

class PestDetailView(generics.RetrieveAPIView):
    queryset = Pest.objects.all()
    serializer_class = PestSerializer
    lookup_field = 'id'

