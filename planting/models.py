from django.db import models
from sites.models import MonitoringSite


class PlantingEvent(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    site = models.ForeignKey(
        MonitoringSite,
        on_delete=models.PROTECT,
        related_name='planting_events'
    )
    planting_date = models.DateField()
    species_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200, blank=True)
    quantity_planted = models.PositiveIntegerField()
    planting_method = models.CharField(max_length=100, blank=True,
        help_text="e.g. seedling, direct seed, cutting")
    planted_by = models.CharField(max_length=200, blank=True,
        help_text="Organisation or team responsible")
    funding_source = models.CharField(max_length=200, blank=True,
        help_text="e.g. Reforest Action, DEA&DP, LandCare")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species_name} × {self.quantity_planted} @ {self.site.name} ({self.planting_date})"

    class Meta:
        ordering = ['-planting_date']


class SurvivalCheck(models.Model):
    CHECK_CHOICES = [
        ('3_month', '3 Month Check'),
        ('6_month', '6 Month Check'),
        ('12_month', '12 Month Check'),
        ('24_month', '24 Month Check'),
        ('adhoc', 'Ad Hoc Check'),
    ]

    planting_event = models.ForeignKey(
        PlantingEvent,
        on_delete=models.PROTECT,
        related_name='survival_checks'
    )
    check_date = models.DateField()
    check_type = models.CharField(max_length=20, choices=CHECK_CHOICES)
    plants_surviving = models.PositiveIntegerField()
    survival_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Auto-calculated as percentage"
    )
    notes = models.TextField(blank=True)
    checked_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.planting_event.quantity_planted > 0:
            self.survival_rate = (
                self.plants_surviving / self.planting_event.quantity_planted
            ) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.planting_event} — {self.get_check_type_display()} ({self.survival_rate}%)"

    class Meta:
        ordering = ['-check_date']