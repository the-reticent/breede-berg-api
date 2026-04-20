from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from organisations.models import OrganisationMembership


def get_user_org(user):
    if user.is_superuser:
        return None
    try:
        return user.membership.organisation
    except OrganisationMembership.DoesNotExist:
        return None


class PlanFeaturePermission(BasePermission):
    """
    Base class. Set `feature` on subclasses.
    Superusers always pass. Orgs without a plan default to starter.
    """
    feature = None

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.is_superuser:
            return True
        org = get_user_org(request.user)
        if org is None:
            return True
        if not org.can_use_feature(self.feature):
            raise PermissionDenied(
                f"Your current plan ({org.get_plan_display()}) does not include "
                f"this feature. Please upgrade to access it."
            )
        return True


class SiteLimitPermission(BasePermission):
    """Enforce max_sites limit on POST to /sites/."""

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        if request.user.is_superuser:
            return True
        org = get_user_org(request.user)
        if org is None:
            return True
        remaining = org.sites_remaining()
        if remaining is not None and remaining <= 0:
            limits = org.get_limits()
            raise PermissionDenied(
                f"You have reached the site limit for your {org.get_plan_display()} plan "
                f"({limits['max_sites']} sites). Please upgrade to add more monitoring sites."
            )
        return True


class UserLimitPermission(BasePermission):
    """Enforce max_users limit on POST to /memberships/."""

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        if request.user.is_superuser:
            return True
        org = get_user_org(request.user)
        if org is None:
            return True
        remaining = org.users_remaining()
        if remaining is not None and remaining <= 0:
            limits = org.get_limits()
            raise PermissionDenied(
                f"You have reached the user limit for your {org.get_plan_display()} plan "
                f"({limits['max_users']} users). Please upgrade to add more team members."
            )
        return True


# Feature-specific permission classes
class VegetationPermission(PlanFeaturePermission):
    feature = 'vegetation'

class WildlifePermission(PlanFeaturePermission):
    feature = 'wildlife'

class PlantingPermission(PlanFeaturePermission):
    feature = 'planting'

class PhotoPermission(PlanFeaturePermission):
    feature = 'photos'

class ExcelImportPermission(PlanFeaturePermission):
    feature = 'excel_import'

class FunderReportPermission(PlanFeaturePermission):
    feature = 'funder_report'

class MultiOrgPermission(PlanFeaturePermission):
    feature = 'multi_org'