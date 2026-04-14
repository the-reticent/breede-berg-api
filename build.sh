#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata monitoring_sites
python manage.py loaddata wildlife_sightings
python manage.py loaddata water_quality_readings
python manage.py loaddata vegetation_surveys