import requests
import math
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from sites.models import MonitoringSite
from wildlife.models import WildlifeSighting


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def find_nearest_site(lat, lon, sites, max_km=5):
    nearest = None
    min_dist = float('inf')
    for site in sites:
        dist = haversine_km(lat, lon, float(site.latitude), float(site.longitude))
        if dist < min_dist:
            min_dist = dist
            nearest = site
    if min_dist <= max_km:
        return nearest
    return None

def get_taxon_type(taxon):
    if not taxon:
        return 'unknown'
    ancestry = taxon.get('ancestry', '') or ''
    iconic = taxon.get('iconic_taxon_name', '') or ''
    name = taxon.get('name', '') or ''

    if iconic in ['Plantae', 'Fungi']:
        return iconic.lower()
    if iconic in ['Aves', 'Mammalia', 'Reptilia', 'Amphibia', 'Actinopterygii', 'Insecta', 'Arachnida']:
        return 'animalia'
    if 'Plantae' in ancestry:
        return 'plantae'
    if 'Animalia' in ancestry:
        return 'animalia'
    if 'Fungi' in ancestry:
        return 'fungi'
    return 'unknown'

class Command(BaseCommand):
    help = 'Sync wildlife observations from iNaturalist for all monitoring sites'

    def add_arguments(self, parser):
        parser.add_argument('--radius', type=int, default=5,
            help='Search radius in km around each site (default: 5)')
        parser.add_argument('--days', type=int, default=30,
            help='Fetch observations from last N days (default: 30)')
        parser.add_argument('--limit', type=int, default=50,
            help='Max observations per site (default: 50)')
        parser.add_argument('--animals-only', action='store_true', 
            help='Only sync animal observations')

    def handle(self, *args, **options):
        sites = list(MonitoringSite.objects.all())
        radius = options['radius']
        days = options['days']
        limit = options['limit']
        if options['animals_only']:
            params['taxon_name'] = 'Animalia'

        created_total = 0
        skipped_total = 0

        self.stdout.write(f"Syncing iNaturalist observations for {len(sites)} sites...")

        for site in sites:
            self.stdout.write(f"  Fetching for: {site.name}")

            url = "https://api.inaturalist.org/v1/observations"
            params = {
                'lat': float(site.latitude),
                'lng': float(site.longitude),
                'radius': radius,
                'order': 'desc',
                'order_by': 'created_at',
                'per_page': limit,
                'd1': (timezone.now() - timezone.timedelta(days=days)).strftime('%Y-%m-%d'),
                'quality_grade': 'research',
                'has[]': 'taxon',
            }

            try:
                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"    Failed to fetch: {e}"))
                continue

            for obs in data.get('results', []):
                inat_id = str(obs.get('id', ''))

                if WildlifeSighting.objects.filter(inaturalist_id=inat_id).exists():
                    skipped_total += 1
                    continue

                taxon = obs.get('taxon') or {}
                species_name = taxon.get('name', 'Unknown species')
                common_name = taxon.get('preferred_common_name', '')

                observed_on = obs.get('observed_on') or obs.get('created_at', '')[:10]
                try:
                    observed_at = timezone.make_aware(
                        datetime.strptime(observed_on, '%Y-%m-%d')
                    )
                except Exception:
                    observed_at = timezone.now()

                obs_lat = obs.get('location', '').split(',')[0] if obs.get('location') else None
                obs_lon = obs.get('location', '').split(',')[1] if obs.get('location') and ',' in obs.get('location') else None

                matched_site = site
                if obs_lat and obs_lon:
                    try:
                        nearest = find_nearest_site(float(obs_lat), float(obs_lon), sites, max_km=radius)
                        if nearest:
                            matched_site = nearest
                    except Exception:
                        pass

                WildlifeSighting.objects.create(
                    site=matched_site,
                    observed_at=observed_at,
                    species_name=species_name,
                    common_name=common_name.title() if common_name else '',
                    count=1,
                    source='inaturalist',
                    taxon_type=get_taxon_type(taxon),
                    inaturalist_id=inat_id,
                    inaturalist_url=f"https://www.inaturalist.org/observations/{inat_id}",
                    notes=f"Synced from iNaturalist. Observer: {obs.get('user', {}).get('login', 'unknown')}"
                )
                created_total += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created: {created_total} new sightings. Skipped {skipped_total} duplicates."
        ))