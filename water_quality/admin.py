from django.contrib import admin
from .models import WaterQualityReading

@admin.register(WaterQualityReading)
class WaterQualityReadingAdmin(admin.ModelAdmin):
    list_display = ['site', 'recorded_at', 'ph', 'dissolved_oxygen', 'temperature', 'turbidity']
    list_filter = ['site', 'recorded_at']
    search_fields = ['notes', 'site__name']
    ordering = ['-recorded_at']