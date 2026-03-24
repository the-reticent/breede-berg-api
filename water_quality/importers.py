import openpyxl
from datetime import datetime
from .models import WaterQualityReading
from sites.models import MonitoringSite


def import_water_quality_excel(file):
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    results = {
        'created': 0,
        'errors': []
    }

    # Skip header row, start from row 2
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        # Skip completely empty rows
        if not any(row):
            continue

        try:
            site_name, recorded_at, ph, dissolved_oxygen, turbidity, temperature, conductivity, notes = row[:8]

            # Validate required fields
            if not site_name:
                results['errors'].append(f"Row {row_num}: site name is required")
                continue

            if not recorded_at:
                results['errors'].append(f"Row {row_num}: recorded_at is required")
                continue

            # Look up the site by name
            try:
                site = MonitoringSite.objects.get(name__iexact=str(site_name).strip())
            except MonitoringSite.DoesNotExist:
                results['errors'].append(f"Row {row_num}: site '{site_name}' not found — create it first")
                continue

            # Handle date parsing if it comes in as a string
            if isinstance(recorded_at, str):
                try:
                    recorded_at = datetime.strptime(recorded_at, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        recorded_at = datetime.strptime(recorded_at, "%Y-%m-%d")
                    except ValueError:
                        results['errors'].append(f"Row {row_num}: invalid date format '{recorded_at}' — use YYYY-MM-DD")
                        continue

            WaterQualityReading.objects.create(
                site=site,
                recorded_at=recorded_at,
                ph=ph or None,
                dissolved_oxygen=dissolved_oxygen or None,
                turbidity=turbidity or None,
                temperature=temperature or None,
                conductivity=conductivity or None,
                notes=notes or ''
            )
            results['created'] += 1

        except Exception as e:
            results['errors'].append(f"Row {row_num}: unexpected error — {str(e)}")

    return results