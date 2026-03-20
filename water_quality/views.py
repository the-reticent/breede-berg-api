from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import WaterQualityReading
from .serializers import WaterQualityReadingSerializer

class WaterQualityReadingViewSet(viewsets.ModelViewSet):
    queryset = WaterQualityReading.objects.all()
    serializer_class = WaterQualityReadingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site', 'recorded_at']
    search_fields = ['notes']
    ordering_fields = ['recorded_at', 'ph', 'temperature']