from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import VegetationSurvey
from .serializers import VegetationSurveySerializer

class VegetationSurveyViewSet(viewsets.ModelViewSet):
    queryset = VegetationSurvey.objects.all()
    serializer_class = VegetationSurveySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site', 'invasive', 'surveyed_at']
    search_fields = ['species_name', 'common_name', 'notes']
    ordering_fields = ['surveyed_at', 'cover_percentage']