"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from sites.views import MonitoringSiteViewSet
from water_quality.views import WaterQualityReadingViewSet
from water_quality.import_views import WaterQualityImportView
from vegetation.views import VegetationSurveyViewSet
from wildlife.views import WildlifeSightingViewSet
from photos.views import SitePhotoViewSet
from planting.views import PlantingEventViewSet, SurvivalCheckViewSet

router = DefaultRouter()
router.register(r'sites', MonitoringSiteViewSet)
router.register(r'water-quality', WaterQualityReadingViewSet)
router.register(r'vegetation', VegetationSurveyViewSet)
router.register(r'wildlife', WildlifeSightingViewSet)
router.register(r'photos', SitePhotoViewSet)
router.register(r'planting-events', PlantingEventViewSet)
router.register(r'survival-checks', SurvivalCheckViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', obtain_auth_token, name='api-token'),
    path('api/v1/import/water-quality/', WaterQualityImportView.as_view(), name='import-water-quality'),
    path('api/v1/', include(router.urls)),
    path('', include('dashboard.urls')),
    path('field/', include('field.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)