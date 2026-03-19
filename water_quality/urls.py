from rest_framework.routers import DefaultRouter
from .views import WaterQualityReadingViewSet

router = DefaultRouter()
router.register(r'readings', WaterQualityReadingViewSet)

urlpatterns = router.urls