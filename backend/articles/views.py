from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, GovernmentResource
from .serializers import ArticleSerializer, GovernmentResourceSerializer
from .mongo_service import save_document_advisory, get_document_advisories

# Imports for Global Search
from crops.models import Crop
from crops.serializers import CropSerializer
from pests.models import Pest
from pests.serializers import PestSerializer
from pesticides.models import Pesticide
from pesticides.serializers import PesticideSerializer
from fertilizers.models import Fertilizer
from fertilizers.serializers import FertilizerSerializer
from diseases.models import Disease
from diseases.serializers import DiseaseSerializer

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        is_scheme = self.request.query_params.get('scheme')

        if category:
            qs = qs.filter(category=category)
        if is_scheme is not None:
            qs = qs.filter(is_government_scheme=(is_scheme.lower() == 'true'))
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(summary__icontains=search)
        return qs

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

class GovernmentResourceListView(generics.ListAPIView):
    queryset = GovernmentResource.objects.all()
    serializer_class = GovernmentResourceSerializer
    permission_classes = [permissions.AllowAny]

class GlobalSearchView(APIView):
    """
    Unified search across all agricultural domains:
    Crops, Pests, Pesticides, Fertilizers, Diseases, Articles.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query or len(query) < 2:
            return Response({
                'query': query,
                'total_results': 0,
                'crops': [],
                'pests': [],
                'pesticides': [],
                'fertilizers': [],
                'diseases': [],
                'articles': []
            })

        crops = Crop.objects.filter(name__icontains=query) | Crop.objects.filter(ideal_soil__icontains=query)
        pests = Pest.objects.filter(pest_name__icontains=query) | Pest.objects.filter(affected_crops__icontains=query)
        pesticides = Pesticide.objects.filter(product_name__icontains=query) | Pesticide.objects.filter(active_ingredient__icontains=query) | Pesticide.objects.filter(target_pests__icontains=query)
        fertilizers = Fertilizer.objects.filter(name__icontains=query) | Fertilizer.objects.filter(category__icontains=query)
        diseases = Disease.objects.filter(disease_name__icontains=query) | Disease.objects.filter(crop__icontains=query)
        articles = Article.objects.filter(title__icontains=query) | Article.objects.filter(category__icontains=query)

        total = crops.count() + pests.count() + pesticides.count() + fertilizers.count() + diseases.count() + articles.count()

        return Response({
            'query': query,
            'total_results': total,
            'crops': CropSerializer(crops[:5], many=True).data,
            'pests': PestSerializer(pests[:5], many=True).data,
            'pesticides': PesticideSerializer(pesticides[:5], many=True).data,
            'fertilizers': FertilizerSerializer(fertilizers[:5], many=True).data,
            'diseases': DiseaseSerializer(diseases[:5], many=True).data,
            'articles': ArticleSerializer(articles[:5], many=True).data,
        })

