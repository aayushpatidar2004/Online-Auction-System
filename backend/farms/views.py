from rest_framework import generics, permissions
from .models import Farm
from .serializers import FarmSerializer

class FarmListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Farm.objects.filter(user=self.request.user)
            # If farmer has no farms yet, return public/demo farms
            if not qs.exists():
                return Farm.objects.filter(user__isnull=True)
            return qs
        return Farm.objects.filter(user__isnull=True)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save(user=None)

class FarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

