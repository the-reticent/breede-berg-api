from django.contrib import admin
from .models import VegetationSurvey

@admin.register(VegetationSurvey)
class VegetationSurveyAdmin(admin.ModelAdmin):
    list_display = ['site', 'species_name', 'common_name', 'cover_percentage', 'invasive', 'surveyed_at']
    list_filter = ['site', 'invasive', 'surveyed_at']
    search_fields = ['species_name', 'common_name', 'notes']
    ordering = ['-surveyed_at']