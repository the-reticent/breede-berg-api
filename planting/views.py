from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import PlantingEvent, SurvivalCheck
from .serializers import PlantingEventSerializer, SurvivalCheckSerializer


class PlantingEventViewSet(viewsets.ModelViewSet):
    queryset = PlantingEvent.objects.all()
    serializer_class = PlantingEventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site', 'status', 'funding_source', 'planting_date']
    search_fields = ['species_name', 'common_name', 'planted_by', 'funding_source']
    ordering_fields = ['planting_date', 'quantity_planted']


class SurvivalCheckViewSet(viewsets.ModelViewSet):
    queryset = SurvivalCheck.objects.all()
    serializer_class = SurvivalCheckSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['planting_event', 'check_type']
    ordering_fields = ['check_date', 'survival_rate']