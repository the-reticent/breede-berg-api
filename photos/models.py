from django.db import models

class SitePhoto(models.Model):
    CATEGORY_CHOICES = [
        ('water_quality', 'Water Quality'),
        ('vegetation', 'Vegetation'),
        ('wildlife', 'Wildlife'),
        ('planting', 'Planting Event'),
        ('general', 'General Site'),
    ]

    site = models.ForeignKey(
        'sites.MonitoringSite',
        on_delete=models.PROTECT,
        related_name='photos'
    )
    image = models.ImageField(upload_to='site_photos/%Y/%m/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    caption = models.CharField(max_length=300, blank=True)
    recorded_at = models.DateTimeField()
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='uploaded_photos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site.name} — {self.category} — {self.recorded_at.date()}"

    class Meta:
        ordering = ['-recorded_at']