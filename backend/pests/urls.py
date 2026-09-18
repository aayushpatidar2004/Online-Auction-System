from django.urls import path
from .views import PestListView, PestDetailView

urlpatterns = [
    path('', PestListView.as_view(), name='pest-list'),
    path('<int:id>/', PestDetailView.as_view(), name='pest-detail'),
]

