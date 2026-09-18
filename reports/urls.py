from django.urls import path
from .views import PriceCsvExportView

urlpatterns = [
    path('price-csv/', PriceCsvExportView.as_view(), name='price-csv'),
]
