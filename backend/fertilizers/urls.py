from django.urls import path
from .views import FertilizerListView, FertilizerDetailView

urlpatterns = [
    path('', FertilizerListView.as_view(), name='fertilizer-list'),
    path('<int:id>/', FertilizerDetailView.as_view(), name='fertilizer-detail'),
]
