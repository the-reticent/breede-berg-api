from django.contrib import admin
from .models import MonitoringSite

@admin.register(MonitoringSite)
class MonitoringSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'river', 'latitude', 'longitude', 'created_at']
    list_filter = ['river']
    search_fields = ['name', 'description']
    ordering = ['river', 'name']
