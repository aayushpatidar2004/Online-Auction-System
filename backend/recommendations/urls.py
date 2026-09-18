from django.urls import path
from .views import CropRecommendView, IrrigationSuggestView

urlpatterns = [
    path('crop/', CropRecommendView.as_view(), name='recommend-crop'),
    path('irrigation/', IrrigationSuggestView.as_view(), name='recommend-irrigation'),
]

