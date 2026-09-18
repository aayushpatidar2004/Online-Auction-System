"""
AgriSmart API URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from articles.views import GlobalSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/weather/', include('weather.urls')),
    path('api/soil/', include('soil.urls')),
    path('api/crops/', include('crops.urls')),
    path('api/diseases/', include('diseases.urls')),
    path('api/plant/', include('diseases.plant_urls')),
    path('api/pests/', include('pests.urls')),
    path('api/pesticides/', include('pesticides.urls')),
    path('api/fertilizers/', include('fertilizers.urls')),
    path('api/farms/', include('farms.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/articles/', include('articles.urls')),
    path('api/search/', GlobalSearchView.as_view(), name='global-search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

