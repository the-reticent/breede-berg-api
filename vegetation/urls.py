from rest_framework.routers import DefaultRouter
from .views import VegetationSurveyViewSet

router = DefaultRouter()
router.register(r'surveys', VegetationSurveyViewSet)

urlpatterns = router.urls