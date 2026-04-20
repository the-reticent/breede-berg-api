from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Organisation, OrganisationMembership
from .serializers import OrganisationSerializer, OrganisationMembershipSerializer
from .plans.permissions import UserLimitPermission

class OrganisationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Organisation.objects.none()
        if user.is_superuser:
            return Organisation.objects.all()
        try:
            membership = user.membership
            if membership.organisation.is_superorg:
                return Organisation.objects.all()
            return Organisation.objects.filter(id=membership.organisation.id)
        except OrganisationMembership.DoesNotExist:
            return Organisation.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class OrganisationMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationMembershipSerializer
    permission_classes = [IsAdminUser, UserLimitPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return OrganisationMembership.objects.all()
        try:
            return OrganisationMembership.objects.filter(
                organisation=user.membership.organisation
            )
        except OrganisationMembership.DoesNotExist:
            return OrganisationMembership.objects.none()