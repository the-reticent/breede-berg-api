from django.contrib import admin
from .models import PlantingEvent, SurvivalCheck


class SurvivalCheckInline(admin.TabularInline):
    model = SurvivalCheck
    extra = 1
    readonly_fields = ['survival_rate']
    fields = ['check_type', 'check_date', 'plants_surviving', 'survival_rate', 'checked_by', 'notes']


@admin.register(PlantingEvent)
class PlantingEventAdmin(admin.ModelAdmin):
    list_display = ['species_name', 'site', 'planting_date', 'quantity_planted', 'funding_source', 'status']
    list_filter = ['site', 'status', 'funding_source']
    search_fields = ['species_name', 'common_name', 'planted_by']
    ordering = ['-planting_date']
    inlines = [SurvivalCheckInline]


@admin.register(SurvivalCheck)
class SurvivalCheckAdmin(admin.ModelAdmin):
    list_display = ['planting_event', 'check_type', 'check_date', 'plants_surviving', 'survival_rate']
    list_filter = ['check_type']
    readonly_fields = ['survival_rate']
    ordering = ['-check_date']