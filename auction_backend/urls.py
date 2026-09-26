from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auctions.views import AuctionViewSet
from payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet, basename='auction')
router.register(r'payments', PaymentViewSet, basename='payment')


def frontend_index(request):
    frontend_index_path = settings.BASE_DIR / 'auction-frontend' / 'build' / 'index.html'
    if not frontend_index_path.exists():
        raise Http404('Frontend build not found. Deploy the React frontend separately or build it before serving.')
    return TemplateView.as_view(template_name='index.html')(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    re_path(r'^(?!api/|admin/|api-auth/).*$', frontend_index),
]
