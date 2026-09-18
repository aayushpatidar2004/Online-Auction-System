from django.urls import path
from .views import CurrentWeatherView, WeatherForecastView, RainfallSummaryView

urlpatterns = [
    path('current/', CurrentWeatherView.as_view(), name='weather-current'),
    path('forecast/', WeatherForecastView.as_view(), name='weather-forecast'),
    path('rainfall/', RainfallSummaryView.as_view(), name='weather-rainfall'),
]

