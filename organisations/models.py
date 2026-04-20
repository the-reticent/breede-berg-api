from django.db import models
from django.contrib.auth.models import User


PLAN_LIMITS = {
    'starter': {
        'max_sites': 5,
        'max_users': 2,
        'water_quality': True,
        'vegetation': False,
        'wildlife': False,
        'planting': False,
        'photos': False,
        'excel_import': False,
        'field_form': False,
        'dashboard': False,
        'inaturalist': False,
        'funder_report': False,
        'multi_org': False,
    },
    'professional': {
        'max_sites': 25,
        'max_users': 5,
        'water_quality': True,
        'vegetation': True,
        'wildlife': True,
        'planting': True,
        'photos': True,
        'excel_import': True,
        'field_form': True,
        'dashboard': True,
        'inaturalist': True,
        'funder_report': False,
        'multi_org': False,
    },
    'programme': {
        'max_sites': None,
        'max_users': None,
        'water_quality': True,
        'vegetation': True,
        'wildlife': True,
        'planting': True,
        'photos': True,
        'excel_import': True,
        'field_form': True,
        'dashboard': True,
        'inaturalist': True,
        'funder_report': True,
        'multi_org': True,
    },
}


class Organisation(models.Model):
    PLAN_CHOICES = [
        ('starter', 'Starter — R1,500/month'),
        ('professional', 'Professional — R4,500/month'),
        ('programme', 'Programme — R10,000/month'),
    ]
    TYPE_CHOICES = [
        ('implementing', 'Implementing Partner'),
        ('funder', 'Funder'),
        ('government', 'Government'),
        ('npo', 'NPO'),
        ('research', 'Research Institution'),
    ]

    name = models.CharField(max_length=200, unique=True)
    org_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='starter')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_superorg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_plan_display()})"

    def get_limits(self):
        return PLAN_LIMITS.get(self.plan, PLAN_LIMITS['starter'])

    def can_use_feature(self, feature):
        return self.get_limits().get(feature, False)

    def sites_remaining(self):
        limit = self.get_limits()['max_sites']
        if limit is None:
            return None
        current = self.sites.count()
        return max(0, limit - current)

    def users_remaining(self):
        limit = self.get_limits()['max_users']
        if limit is None:
            return None
        current = self.memberships.count()
        return max(0, limit - current)

    class Meta:
        ordering = ['name']


class OrganisationMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('field_worker', 'Field Worker'),
        ('viewer', 'Viewer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='field_worker')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.organisation.name} ({self.role})"