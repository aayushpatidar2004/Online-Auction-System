import sys
from pathlib import Path
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Disease, PlantAnalysis
from .serializers import DiseaseSerializer, PlantAnalysisSerializer

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.plant_disease.disease_classifier import analyze_leaf_image

class DiseaseListView(generics.ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        crop = self.request.query_params.get('crop')
        search = self.request.query_params.get('search')
        if crop:
            qs = qs.filter(crop__icontains=crop)
        if search:
            qs = qs.filter(disease_name__icontains=search)
        return qs

class DiseaseDetailView(generics.RetrieveAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    lookup_field = 'id'

class PlantAnalyzeImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image file uploaded. Please upload a leaf or plant image.'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        # Validate file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return Response({'error': 'Image file exceeds maximum 5MB limit. Please upload a compressed image.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate content type
        if not image_file.content_type.startswith('image/'):
            return Response({'error': 'Invalid file format. Please upload a JPG, PNG, or WebP image.'}, status=status.HTTP_400_BAD_REQUEST)

        # Run diagnosis through modular ML pipeline
        diagnostic_result = analyze_leaf_image(image_file)

        # Save scan record
        try:
            user = request.user if request.user.is_authenticated else None
            scan = PlantAnalysis.objects.create(
                user=user,
                image=image_file,
                plant_name=diagnostic_result.get('plant', 'Crop'),
                detected_condition=diagnostic_result.get('disease_name', 'Unknown'),
                confidence=diagnostic_result.get('confidence', 0.0),
                severity=diagnostic_result.get('severity', 'Moderate'),
                is_healthy=diagnostic_result.get('is_healthy', False)
            )
            diagnostic_result['scan_id'] = scan.id
            diagnostic_result['image_url'] = scan.image.url
        except Exception:
            pass

        return Response(diagnostic_result)

