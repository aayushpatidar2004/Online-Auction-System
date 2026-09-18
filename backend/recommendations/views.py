import sys
import os
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crops.models import Crop

# Add project root to sys.path to access ml modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.crop_recommendation.train_model import predict_crops

class CropRecommendView(APIView):
    """
    POST /api/recommendations/crop/ or /api/crops/recommend/
    Input: N, P, K, temperature, humidity, ph, rainfall, soil_type
    Output: Top recommended crops with confidence score and crop profile.
    """
    def post(self, request):
        data = request.data
        try:
            n = float(data.get('N', data.get('nitrogen', 90)))
            p = float(data.get('P', data.get('phosphorus', 42)))
            k = float(data.get('K', data.get('potassium', 43)))
            temp = float(data.get('temperature', 25))
            humidity = float(data.get('humidity', 80))
            ph = float(data.get('ph', 6.5))
            rainfall = float(data.get('rainfall', 200))
            soil_type = data.get('soil_type', 'Alluvial Soil')
        except (ValueError, TypeError) as e:
            return Response({'error': f'Invalid numeric parameter: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Predict using ML model
        predictions = predict_crops(
            n=n, p=p, k=k,
            temperature=temp,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            soil_type=soil_type,
            top_k=3
        )

        # Enrich with database crop info if available
        enriched = []
        for item in predictions:
            crop_obj = Crop.objects.filter(name__iexact=item['crop']).first()
            enriched.append({
                **item,
                'season': crop_obj.season if crop_obj else 'Kharif / Rabi',
                'water_requirement': crop_obj.water_requirement if crop_obj else 'Moderate',
                'ideal_soil': crop_obj.ideal_soil if crop_obj else soil_type,
                'description': crop_obj.description if crop_obj else f"High economic return crop well-suited for N={n}, P={p}, K={k} and rainfall of {rainfall}mm.",
                'image_url': crop_obj.image_url if crop_obj and crop_obj.image_url else ''
            })

        return Response({
            'inputs': {
                'N': n, 'P': p, 'K': k,
                'temperature': temp, 'humidity': humidity,
                'ph': ph, 'rainfall': rainfall, 'soil_type': soil_type
            },
            'recommendations': enriched,
            'confidence_supported': True,
            'summary': f"Based on your soil nutrients (N:{n}, P:{p}, K:{k}) and weather profile, {enriched[0]['crop']} is the primary recommendation with {enriched[0]['confidence']}% confidence."
        })

class IrrigationSuggestView(APIView):
    """
    POST /api/recommendations/irrigation/
    Input: temperature, humidity, rainfall, soil_moisture, crop, soil_type
    """
    def post(self, request):
        data = request.data
        try:
            temp = float(data.get('temperature', 30))
            humidity = float(data.get('humidity', 60))
            rainfall = float(data.get('rainfall', 0))
            moisture = float(data.get('soil_moisture', 38))
            crop_name = data.get('crop', 'Cotton')
            soil_type = data.get('soil_type', 'Black Soil')
        except (ValueError, TypeError) as e:
            return Response({'error': f'Invalid input: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Crop-specific moisture thresholds (percentage)
        CROP_THRESHOLDS = {
            'rice': {'min': 70, 'opt': 85, 'type': 'High water submergence'},
            'sugarcane': {'min': 55, 'opt': 75, 'type': 'High water'},
            'cotton': {'min': 40, 'opt': 60, 'type': 'Moderate water, sensitive to waterlogging'},
            'wheat': {'min': 45, 'opt': 65, 'type': 'Crown root initiation & flowering sensitive'},
            'maize': {'min': 45, 'opt': 65, 'type': 'Tasseling & silking sensitive'},
            'soybean': {'min': 40, 'opt': 60, 'type': 'Pod filling sensitive'},
            'groundnut': {'min': 35, 'opt': 55, 'type': 'Pegging sensitive'},
            'chickpea': {'min': 30, 'opt': 50, 'type': 'Low water requirement'},
        }

        crop_key = crop_name.lower().split()[0]
        threshold = CROP_THRESHOLDS.get(crop_key, {'min': 40, 'opt': 60, 'type': 'Standard'})
        min_moisture = threshold['min']

        # Determine irrigation urgency
        if moisture < min_moisture and rainfall < 5.0:
            if moisture < min_moisture - 15:
                urgency = "Immediate Irrigation Required"
                badge = "danger"
                action_text = f"Soil moisture ({moisture}%) is critically below the minimum threshold ({min_moisture}%) for {crop_name}. Immediate watering recommended."
            else:
                urgency = "Irrigation Recommended within 24-48 Hours"
                badge = "warning"
                action_text = f"Soil moisture ({moisture}%) is dipping below the optimal threshold ({min_moisture}%). Provide light irrigation, preferably in early morning or evening."
        elif rainfall >= 10.0:
            urgency = "Withhold Irrigation (Rainfall Anticipated)"
            badge = "info"
            action_text = f"Upcoming rainfall of {rainfall} mm will provide natural moisture replenishment. Hold irrigation to prevent root hypoxia and waterlogging."
        elif moisture > threshold['opt'] + 15:
            urgency = "Excess Moisture Detected"
            badge = "warning"
            action_text = f"Soil moisture is high ({moisture}%). Ensure adequate surface field drainage to avoid root fungal infection."
        else:
            urgency = "Adequate Soil Moisture"
            badge = "success"
            action_text = f"Soil moisture ({moisture}%) is within the healthy zone for {crop_name}. Continue daily monitoring."

        return Response({
            'crop': crop_name,
            'soil_type': soil_type,
            'soil_moisture': moisture,
            'critical_threshold': min_moisture,
            'status': urgency,
            'badge': badge,
            'action_recommendation': action_text,
            'crop_sensitivity_note': threshold['type'],
            'disclaimer': "Irrigation requirements vary by crop growth stage, soil texture, local wind, and ambient humidity. Use this advice in conjunction with local field observations."
        })

