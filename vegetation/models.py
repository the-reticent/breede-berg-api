from django.db import models
from sites.models import MonitoringSite

class VegetationSurvey(models.Model):
    site = models.ForeignKey(
        MonitoringSite,
        on_delete=models.PROTECT,
        related_name='vegetation_surveys'
    )
    surveyed_at = models.DateField()
    species_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200, blank=True)
    cover_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invasive = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species_name} @ {self.site.name}"

    class Meta:
        ordering = ['-surveyed_at']