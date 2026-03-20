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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sites.views import MonitoringSiteViewSet
from water_quality.views import WaterQualityReadingViewSet
from vegetation.views import VegetationSurveyViewSet
from wildlife.views import WildlifeSightingViewSet

router = DefaultRouter()
router.register(r'sites', MonitoringSiteViewSet)
router.register(r'water-quality', WaterQualityReadingViewSet)
router.register(r'vegetation', VegetationSurveyViewSet)
router.register(r'wildlife', WildlifeSightingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
