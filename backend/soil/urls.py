from django.urls import path
from .views import SoilTypesListView, SoilAnalyzeView

urlpatterns = [
    path('types/', SoilTypesListView.as_view(), name='soil-types'),
    path('analyze/', SoilAnalyzeView.as_view(), name='soil-analyze'),
]

