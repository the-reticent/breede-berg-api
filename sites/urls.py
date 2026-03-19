from rest_framework.routers import DefaultRouter
from .views import MonitoringSiteViewSet

router = DefaultRouter()
router.register(r'sites', MonitoringSiteViewSet)

urlpatterns = router.urls