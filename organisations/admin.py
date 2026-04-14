from django.contrib import admin
from .models import Organisation, OrganisationMembership


class MembershipInline(admin.TabularInline):
    model = OrganisationMembership
    extra = 1
    fields = ['user', 'role']


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_type', 'is_superorg', 'contact_email', 'created_at']
    list_filter = ['org_type', 'is_superorg']
    search_fields = ['name']
    inlines = [MembershipInline]


@admin.register(OrganisationMembership)
class OrganisationMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organisation', 'role', 'created_at']
    list_filter = ['organisation', 'role']