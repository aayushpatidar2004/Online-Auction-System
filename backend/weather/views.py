from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import fetch_current_weather, fetch_weather_forecast, fetch_rainfall_summary
from .models import WeatherRecord

class CurrentWeatherView(APIView):
    def get(self, request):
        village = request.query_params.get('village', '')
        city = request.query_params.get('city', '')
        district = request.query_params.get('district', '')
        state = request.query_params.get('state', '')

        data = fetch_current_weather(village=village, city=city, district=district, state=state)
        
        # Save record for audit/caching
        try:
            WeatherRecord.objects.create(
                location_name=data['location'],
                district=data['district'],
                state=data['state'],
                temperature=data['temperature'],
                humidity=data['humidity'],
                wind_speed=data['wind_speed'],
                condition=data['condition'],
                cloud_percentage=data['cloud_percentage'],
                rainfall_mm=data['rainfall_mm'],
                rain_probability=data['rain_probability'],
                sunrise=data['sunrise'],
                sunset=data['sunset']
            )
        except Exception:
            pass

        return Response(data)

class WeatherForecastView(APIView):
    def get(self, request):
        district = request.query_params.get('district', '')
        state = request.query_params.get('state', '')
        days = int(request.query_params.get('days', 7))
        data = fetch_weather_forecast(district=district, state=state, days=days)
        return Response(data)

class RainfallSummaryView(APIView):
    def get(self, request):
        district = request.query_params.get('district', '')
        state = request.query_params.get('state', '')
        data = fetch_rainfall_summary(district=district, state=state)
        return Response(data)

