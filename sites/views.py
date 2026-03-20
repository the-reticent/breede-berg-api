from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MonitoringSite
from .serializers import MonitoringSiteSerializer

class MonitoringSiteViewSet(viewsets.ModelViewSet):
    queryset = MonitoringSite.objects.all()
    serializer_class = MonitoringSiteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['river']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']