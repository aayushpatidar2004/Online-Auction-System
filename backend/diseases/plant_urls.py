from django.urls import path
from .views import PlantAnalyzeImageView

urlpatterns = [
    path('analyze/', PlantAnalyzeImageView.as_view(), name='plant-analyze'),
]

