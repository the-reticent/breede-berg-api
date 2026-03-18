from django.db import models
from sites.models import MonitoringSite

class WildlifeSighting(models.Model):
    site = models.ForeignKey(
        MonitoringSite,
        on_delete=models.PROTECT,
        related_name='wildlife_sightings'
    )
    observed_at = models.DateTimeField()
    species_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200, blank=True)
    count = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.common_name or self.species_name} @ {self.site.name}"

    class Meta:
        ordering = ['-observed_at']