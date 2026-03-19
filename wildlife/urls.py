from rest_framework.routers import DefaultRouter
from .views import WildlifeSightingViewSet

router = DefaultRouter()
router.register(r'sightings', WildlifeSightingViewSet)

urlpatterns = router.urls