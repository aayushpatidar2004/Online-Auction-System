from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import analyze_soil, SOIL_CROP_MAPPING
from .serializers import SoilAnalysisInputSerializer
from .models import SoilRecord

class SoilTypesListView(APIView):
    def get(self, request):
        types_data = []
        for name, info in SOIL_CROP_MAPPING.items():
            types_data.append({
                'name': name,
                'characteristics': info['characteristics'],
                'suitable_crops': info['crops'],
                'irrigation_factor': info['irrigation_factor']
            })
        return Response({'soil_types': types_data})

class SoilAnalyzeView(APIView):
    def post(self, request):
        serializer = SoilAnalysisInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        analysis = analyze_soil(
            soil_type=d['soil_type'],
            ph=d['ph'],
            nitrogen=d['nitrogen'],
            phosphorus=d['phosphorus'],
            potassium=d['potassium'],
            moisture=d['moisture'],
            organic_carbon=d['organic_carbon']
        )

        # Save record if user is authenticated
        if request.user.is_authenticated:
            try:
                SoilRecord.objects.create(
                    user=request.user,
                    soil_type=d['soil_type'],
                    ph=d['ph'],
                    nitrogen=d['nitrogen'],
                    phosphorus=d['phosphorus'],
                    potassium=d['potassium'],
                    moisture=d['moisture'],
                    organic_carbon=d['organic_carbon'],
                    health_score=analysis['health_score'],
                    health_status=analysis['health_label'],
                    suitable_crops=", ".join(analysis['suitable_crops'][:4])
                )
            except Exception:
                pass

        return Response(analysis)

