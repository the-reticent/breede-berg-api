from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import WildlifeSighting
from .serializers import WildlifeSightingSerializer
from organisations.plans.permissions import WildlifePermission

class WildlifeSightingViewSet(viewsets.ModelViewSet):
    queryset = WildlifeSighting.objects.all()
    serializer_class = WildlifeSightingSerializer
    permission_classes = [WildlifePermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['site', 'observed_at', 'source', 'taxon_type']
    search_fields = ['species_name', 'common_name', 'notes']
    ordering_fields = ['observed_at', 'count']