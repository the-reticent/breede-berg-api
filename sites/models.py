from django.db import models

class MonitoringSite(models.Model):
    RIVER_CHOICES = [
        ('breede', 'Breede River'),
        ('berg', 'Berg River'),
    ]

    name = models.CharField(max_length=200)
    river = models.CharField(max_length=20, choices=RIVER_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=True)
    organisation = models.ForeignKey(
        'organisations.Organisation',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sites',
        help_text="Which organisation manages this site"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_river_display()})"

    class Meta:
        ordering = ['river', 'name']