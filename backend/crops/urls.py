from django.urls import path
from .views import CropListView, CropDetailView

urlpatterns = [
    path('', CropListView.as_view(), name='crop-list'),
    path('<int:id>/', CropDetailView.as_view(), name='crop-detail'),
]

