from django.contrib import admin
from .models import SitePhoto

@admin.register(SitePhoto)
class SitePhotoAdmin(admin.ModelAdmin):
    list_display = ['site', 'category', 'caption', 'recorded_at', 'uploaded_by']
    list_filter = ['site', 'category']
    ordering = ['-recorded_at']