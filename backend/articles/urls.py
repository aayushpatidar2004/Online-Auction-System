from django.urls import path
from .views import ArticleListView, ArticleDetailView, GovernmentResourceListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('resources/', GovernmentResourceListView.as_view(), name='government-resources'),
]
