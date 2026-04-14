from django.db import models
from django.contrib.auth.models import User


class Organisation(models.Model):
    TYPE_CHOICES = [
        ('implementing', 'Implementing Partner'),
        ('funder', 'Funder'),
        ('government', 'Government'),
        ('npo', 'NPO'),
        ('research', 'Research Institution'),
    ]

    name = models.CharField(max_length=200, unique=True)
    org_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_superorg = models.BooleanField(
        default=False,
        help_text="Superorgs like DEA&DP can see all organisations' data"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class OrganisationMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('field_worker', 'Field Worker'),
        ('viewer', 'Viewer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='membership'
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='field_worker')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.organisation.name} ({self.role})"