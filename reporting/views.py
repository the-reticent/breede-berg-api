from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Max, Min, Sum
from django.utils import timezone
from datetime import timedelta

from sites.models import MonitoringSite
from water_quality.models import WaterQualityReading
from vegetation.models import VegetationSurvey
from wildlife.models import WildlifeSighting
from planting.models import PlantingEvent, SurvivalCheck
from organisations.models import Organisation, OrganisationMembership
from organisations.plans.permissions import FunderReportPermission


def get_accessible_orgs(user):
    if user.is_superuser:
        return Organisation.objects.all()
    try:
        membership = user.membership
        if membership.organisation.is_superorg:
            return Organisation.objects.all()
        return Organisation.objects.filter(id=membership.organisation.id)
    except OrganisationMembership.DoesNotExist:
        return Organisation.objects.none()


def get_accessible_sites(user):
    orgs = get_accessible_orgs(user)
    if user.is_superuser:
        return MonitoringSite.objects.all()
    try:
        membership = user.membership
        if membership.organisation.is_superorg:
            return MonitoringSite.objects.all()
        return MonitoringSite.objects.filter(organisation__in=orgs)
    except OrganisationMembership.DoesNotExist:
        return MonitoringSite.objects.none()


class FunderReportView(APIView):
    permission_classes = [IsAuthenticated, FunderReportPermission]

    def get(self, request):
        sites = get_accessible_sites(request.user)
        orgs = get_accessible_orgs(request.user)
        site_ids = sites.values_list('id', flat=True)

        now = timezone.now()
        one_year_ago = now - timedelta(days=365)
        thirty_days_ago = now - timedelta(days=30)

        # --- Programme overview ---
        total_sites = sites.count()
        breede_sites = sites.filter(river='breede').count()
        berg_sites = sites.filter(river='berg').count()

        # --- Planting summary ---
        planting_qs = PlantingEvent.objects.filter(site__in=site_ids)
        total_planted = planting_qs.aggregate(
            total=Sum('quantity_planted')
        )['total'] or 0
        planting_by_species = list(
            planting_qs.values('species_name', 'common_name')
            .annotate(total=Sum('quantity_planted'))
            .order_by('-total')[:10]
        )
        planting_by_funder = list(
            planting_qs.values('funding_source')
            .annotate(total=Sum('quantity_planted'))
            .order_by('-total')
        )

        # --- Survival rates ---
        survival_qs = SurvivalCheck.objects.filter(
            planting_event__site__in=site_ids
        )
        avg_survival = survival_qs.aggregate(
            avg=Avg('survival_rate')
        )['avg']
        latest_survival = survival_qs.order_by('-check_date').first()

        # --- Water quality ---
        wq_qs = WaterQualityReading.objects.filter(site__in=site_ids)
        wq_recent = wq_qs.filter(recorded_at__gte=one_year_ago)
        wq_averages = wq_recent.aggregate(
            avg_ph=Avg('ph'),
            avg_temperature=Avg('temperature'),
            avg_dissolved_oxygen=Avg('dissolved_oxygen'),
            avg_turbidity=Avg('turbidity'),
        )
        wq_by_site = list(
            wq_recent.values('site__name', 'site__river')
            .annotate(
                readings=Count('id'),
                avg_ph=Avg('ph'),
                avg_temp=Avg('temperature'),
                avg_do=Avg('dissolved_oxygen'),
            )
            .order_by('site__river', 'site__name')
        )

        # --- Vegetation ---
        veg_qs = VegetationSurvey.objects.filter(site__in=site_ids)
        total_surveys = veg_qs.count()
        invasive_count = veg_qs.filter(invasive=True).count()
        native_count = veg_qs.filter(invasive=False).count()
        top_species = list(
            veg_qs.values('species_name', 'common_name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # --- Wildlife / biodiversity ---
        wl_qs = WildlifeSighting.objects.filter(site__in=site_ids)
        total_sightings = wl_qs.count()
        unique_species = wl_qs.values('species_name').distinct().count()
        inaturalist_count = wl_qs.filter(source='inaturalist').count()
        manual_count = wl_qs.filter(source='manual').count()
        recent_sightings = wl_qs.filter(
            observed_at__gte=thirty_days_ago
        ).count()
        top_wildlife = list(
            wl_qs.values('species_name', 'common_name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # --- Per organisation summary ---
        org_summaries = []
        for org in orgs:
            org_sites = sites.filter(organisation=org)
            org_site_ids = org_sites.values_list('id', flat=True)
            org_summaries.append({
                'organisation': org.name,
                'type': org.get_org_type_display(),
                'sites': org_sites.count(),
                'plants_planted': PlantingEvent.objects.filter(
                    site__in=org_site_ids
                ).aggregate(total=Sum('quantity_planted'))['total'] or 0,
                'water_quality_readings': WaterQualityReading.objects.filter(
                    site__in=org_site_ids
                ).count(),
                'vegetation_surveys': VegetationSurvey.objects.filter(
                    site__in=org_site_ids
                ).count(),
                'wildlife_sightings': WildlifeSighting.objects.filter(
                    site__in=org_site_ids
                ).count(),
            })

        return Response({
            'report_generated_at': now.isoformat(),
            'report_period': {
                'water_quality_from': one_year_ago.date().isoformat(),
                'to': now.date().isoformat(),
            },
            'programme_overview': {
                'total_sites': total_sites,
                'breede_river_sites': breede_sites,
                'berg_river_sites': berg_sites,
                'organisations': orgs.count(),
            },
            'planting': {
                'total_plants_planted': total_planted,
                'planting_events': planting_qs.count(),
                'average_survival_rate': round(float(avg_survival), 1) if avg_survival else None,
                'latest_survival_check': {
                    'date': latest_survival.check_date.isoformat() if latest_survival else None,
                    'rate': float(latest_survival.survival_rate) if latest_survival else None,
                    'type': latest_survival.get_check_type_display() if latest_survival else None,
                },
                'by_species': planting_by_species,
                'by_funder': planting_by_funder,
            },
            'water_quality': {
                'total_readings': wq_qs.count(),
                'readings_last_12_months': wq_recent.count(),
                'averages_last_12_months': {
                    'ph': round(wq_averages['avg_ph'], 2) if wq_averages['avg_ph'] else None,
                    'temperature_c': round(wq_averages['avg_temperature'], 2) if wq_averages['avg_temperature'] else None,
                    'dissolved_oxygen_mgl': round(wq_averages['avg_dissolved_oxygen'], 2) if wq_averages['avg_dissolved_oxygen'] else None,
                    'turbidity_ntu': round(wq_averages['avg_turbidity'], 2) if wq_averages['avg_turbidity'] else None,
                },
                'by_site': wq_by_site,
            },
            'vegetation': {
                'total_surveys': total_surveys,
                'native_species_records': native_count,
                'invasive_species_records': invasive_count,
                'invasive_percentage': round(invasive_count / total_surveys * 100, 1) if total_surveys else 0,
                'top_species': top_species,
            },
            'biodiversity': {
                'total_sightings': total_sightings,
                'unique_species': unique_species,
                'sightings_last_30_days': recent_sightings,
                'from_inaturalist': inaturalist_count,
                'manual_entries': manual_count,
                'top_species': top_wildlife,
            },
            'by_organisation': org_summaries,
        })