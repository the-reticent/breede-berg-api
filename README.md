# Breede & Berg River Monitoring Platform

A production-grade environmental data platform for river restoration monitoring across the Breede and Berg river systems in the Western Cape, South Africa.

Built to replace fragmented Excel-based field data collection with a structured, accessible, and well-documented data platform — bringing modern data engineering practices to ecological restoration work.

---

## The Problem

> *90% of environmental data sits in Excel spreadsheets.*

Field scientists collecting water quality measurements, vegetation surveys, and wildlife sightings have no shared infrastructure. Data lives on individual computers, in disconnected spreadsheets, inaccessible to researchers and policy makers who need it most.

The Berg and Breede Riparian Rehabilitation Programme has planted over 2.16 million plants since 2013. There is currently no system that tracks survival rates, water quality improvement, or biodiversity recovery across sites in a structured, queryable way.

This platform is the bridge.

---

## Live Demo

| URL | Description |
|---|---|
| `/` | Role-aware dashboard — public, field team, programme views |
| `/field/` | Mobile field data capture form |
| `/admin/` | Django admin panel |
| `/api/docs/` | Interactive Swagger / OpenAPI documentation |
| `/api/v1/reports/funder-report/` | Programme summary report |

---

## What It Does

### Data collection
- Mobile field capture form — works on any phone, no app install needed
- Water quality readings (pH, dissolved oxygen, turbidity, temperature, conductivity)
- Vegetation surveys with invasive species flagging
- Wildlife sightings with species identification
- Planting events with species, quantity, funding source, and planting method
- Survival checks at 3, 6, 12 and 24 months with auto-calculated survival rates
- Photo uploads — camera or file picker, attached to any record type
- Excel importer — upload existing spreadsheets directly into the database

### Data intelligence
- iNaturalist sync — pulls research-grade citizen science observations within 5km of each monitoring site automatically
- 609+ biodiversity records synced from iNaturalist across 18 river sites
- Funder reporting endpoint — complete programme summary in a single API call

### Visualisation
- Role-aware dashboard — three views based on who is logged in
  - Public view: headline impact numbers, species map, no login required
  - Field team view: their sites, recent submissions, survival rates, quick actions, field photos
  - Programme view: all organisations, partner performance table, water quality trends, planting by funder, invasive vs native vegetation

### Infrastructure
- Multi-organisation support — per-org data isolation
- Superorg access (funders and government sees all partners, restoration active organisations see only their own data)
- Token authentication — each field worker has their own credentials
- Filtering, search, ordering, and pagination on all endpoints
- Auto-generated Swagger / OpenAPI 3.0 documentation

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL |
| Auth | Token-based authentication (DRF) |
| Filtering | django-filter |
| API Docs | drf-spectacular (Swagger / OpenAPI 3.0) |
| Excel ingestion | openpyxl |
| Image handling | Pillow |
| iNaturalist | requests (public API, no auth required) |
| Maps | Leaflet.js |
| Charts | Chart.js |
| Deployment | Render (web service + PostgreSQL) |

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/sites/` | Monitoring sites | Public |
| GET/POST | `/api/v1/water-quality/` | Water quality readings | GET public, POST token |
| GET/POST | `/api/v1/vegetation/` | Vegetation surveys | GET public, POST token |
| GET/POST | `/api/v1/wildlife/` | Wildlife sightings | GET public, POST token |
| GET/POST | `/api/v1/planting-events/` | Planting events | GET public, POST token |
| GET/POST | `/api/v1/survival-checks/` | Survival rate checks | GET public, POST token |
| GET/POST | `/api/v1/photos/` | Site photography | GET public, POST token |
| GET | `/api/v1/organisations/` | Organisations | Token |
| GET | `/api/v1/reports/funder-report/` | Programme summary | Token |
| POST | `/api/v1/import/water-quality/` | Excel importer | Token |
| POST | `/api/v1/auth/token/` | Obtain token | Public |
| GET | `/api/docs/` | Swagger docs | Public |

---

## iNaturalist Sync

Pull research-grade observations from within 5km of all monitoring sites:

```bash
python manage.py sync_inaturalist
python manage.py sync_inaturalist --days 365 --limit 100
python manage.py sync_inaturalist --radius 10 --days 30
```

---

## Excel Import

Upload `.xlsx` files to bulk-import water quality readings:

```bash
curl -X POST https://your-domain.com/api/v1/import/water-quality/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@your_data.xlsx"
```

Required columns: `site_name`, `recorded_at`, `ph`, `dissolved_oxygen`, `turbidity`, `temperature`, `conductivity`, `notes`

---

## Multi-Organisation Setup

The platform supports multiple implementing partners with isolated data:

- **Superorg** (funders) — sees all organisations and all sites
- **Implementing partner** (active conservation orgs) — sees only their own sites and data
- **Field worker** — submits data via mobile form, sees their organisation's dashboard

---

## Getting Started

```bash
git clone https://github.com/the-reticent/breede-berg-api.git
cd breede-berg-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python manage.py migrate
python manage.py loaddata monitoring_sites
python manage.py createsuperuser
python manage.py runserver
```

---

## Project Structure

```
breede-berg-api/
├── config/              # Django settings and URL routing
├── sites/               # Monitoring sites
├── water_quality/       # Water quality readings + Excel importer
├── vegetation/          # Vegetation surveys
├── wildlife/            # Wildlife sightings + iNaturalist sync
├── planting/            # Planting events + survival checks
├── photos/              # Site photography
├── organisations/       # Multi-org support
├── reporting/           # Funder reporting endpoint
├── dashboard/           # Role-aware dashboard
├── field/               # Mobile field capture form
└── build.sh             # Render deployment script
```

---

## Background

This project was built at the intersection of two industries — telecommunications and environmental restoration. The data infrastructure gap in ecology is striking: while telecoms process terabytes of real-time data through robust pipelines, environmental scientists are still emailing spreadsheets.

The skills that optimise network performance transfer directly to biodiversity databases. REST APIs that connect global infrastructure can connect habitat monitoring systems. This project is proof of that.

---

## Roadmap

- [x] REST API for water quality, vegetation, wildlife
- [x] 18 real monitoring sites — Breede and Berg rivers
- [x] Token authentication
- [x] Excel importer
- [x] Django admin panel
- [x] Mobile field capture form with photo uploads
- [x] Planting events and survival tracking
- [x] iNaturalist integration — 609+ biodiversity records
- [x] Role-aware dashboard — public, field team, programme views
- [x] Multi-organisation support with data isolation
- [x] Funder reporting endpoint
- [x] Deployed on Render
- [ ] Cloudinary integration for persistent photo storage
- [ ] Scheduled iNaturalist sync (daily/weekly)
- [ ] CSV export per organisation
- [ ] Email report delivery to funders

---

## License

MIT

---

## Author

**Kudakwashe Mike Mapaya**
Python Developer · Data Engineer · Environmental Tech

[LinkedIn](https://linkedin.com/in/kudakwashe-mike-mapaya-654281160) · [Email](mailto:kudamapaya@gmail.com) · [GitHub](https://github.com/the-reticent)
