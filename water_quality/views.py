from rest_framework import viewsets
from .models import WaterQualityReading
from .serializers import WaterQualityReadingSerializer

class WaterQualityReadingViewSet(viewsets.ModelViewSet):
    queryset = WaterQualityReading.objects.all()
    serializer_class = WaterQualityReadingSerializer