from django.db import models
from sites.models import MonitoringSite

class WaterQualityReading(models.Model):
    site = models.ForeignKey(
        MonitoringSite,
        on_delete=models.PROTECT,
        related_name='water_quality_readings'
    )
    recorded_at = models.DateTimeField()
    ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    dissolved_oxygen = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    turbidity = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    conductivity = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site.name} — {self.recorded_at.date()}"

    class Meta:
        ordering = ['-recorded_at']