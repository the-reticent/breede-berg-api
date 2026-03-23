from django.contrib import admin
from .models import WildlifeSighting

@admin.register(WildlifeSighting)
class WildlifeSightingAdmin(admin.ModelAdmin):
    list_display = ['site', 'species_name', 'common_name', 'count', 'observed_at']
    list_filter = ['site', 'observed_at']
    search_fields = ['species_name', 'common_name', 'notes']
    ordering = ['-observed_at']