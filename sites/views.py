from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MonitoringSite
from .serializers import MonitoringSiteSerializer
from organisations.models import OrganisationMembership
from organisations.plans.permissions import SiteLimitPermission


class MonitoringSiteViewSet(viewsets.ModelViewSet):
    serializer_class = MonitoringSiteSerializer
    permission_classes = [SiteLimitPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['river', 'organisation']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return MonitoringSite.objects.all()
        if user.is_superuser:
            return MonitoringSite.objects.all()
        try:
            membership = user.membership
            if membership.organisation.is_superorg:
                return MonitoringSite.objects.all()
            return MonitoringSite.objects.filter(organisation=membership.organisation)
        except OrganisationMembership.DoesNotExist:
            return MonitoringSite.objects.all()