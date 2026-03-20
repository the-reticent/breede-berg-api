from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import WildlifeSighting
from .serializers import WildlifeSightingSerializer

class WildlifeSightingViewSet(viewsets.ModelViewSet):
    queryset = WildlifeSighting.objects.all()
    serializer_class = WildlifeSightingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site', 'observed_at']
    search_fields = ['species_name', 'common_name', 'notes']
    ordering_fields = ['observed_at', 'count']