# Breede & Berg River Monitoring API

A production-grade REST API for ecological monitoring data across the Breede and Berg river systems in the Western Cape, South Africa.

Built to replace fragmented Excel-based field data collection with a structured, accessible, and well-documented data platform — bringing modern data engineering practices to environmental restoration work.

---

## The Problem

> *90% of environmental data sits in Excel spreadsheets.*

Field scientists collecting water quality measurements, vegetation surveys, and wildlife sightings have no shared infrastructure. Data lives on individual computers, in disconnected spreadsheets, inaccessible to researchers and policy makers who need it most.

This API is the bridge.

---

## What It Does

- Stores and serves **water quality readings** (pH, dissolved oxygen, turbidity, temperature, conductivity)
- Tracks **vegetation surveys** including species, cover percentage, and invasive status
- Records **wildlife sightings** with species, count, and observation metadata
- Links all data to named **monitoring sites** on the Breede and Berg rivers
- Accepts **Excel file uploads** to ingest existing spreadsheet data automatically
- Exposes a fully **documented, filterable, paginated REST API**

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

---

## API Endpoints

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/api/v1/sites/` | List all monitoring sites | No |
| POST | `/api/v1/sites/` | Create a monitoring site | Yes |
| GET | `/api/v1/water-quality/` | List water quality readings | No |
| POST | `/api/v1/water-quality/` | Add a reading | Yes |
| GET | `/api/v1/vegetation/` | List vegetation surveys | No |
| POST | `/api/v1/vegetation/` | Add a survey | Yes |
| GET | `/api/v1/wildlife/` | List wildlife sightings | No |
| POST | `/api/v1/wildlife/` | Add a sighting | Yes |
| POST | `/api/v1/import/water-quality/` | Upload Excel file to import readings | Yes |
| POST | `/api/v1/auth/token/` | Obtain authentication token | No |
| GET | `/api/docs/` | Interactive Swagger documentation | No |

---

## Filtering & Search

All list endpoints support filtering, search, and ordering:

```bash
# Filter by river
GET /api/v1/sites/?river=breede

# Search by name
GET /api/v1/sites/?search=Rawsonville

# Filter readings by site
GET /api/v1/water-quality/?site=1

# Filter invasive species only
GET /api/v1/vegetation/?invasive=true

# Order by most recent
GET /api/v1/water-quality/?ordering=-recorded_at
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Git

### Installation

```bash
# Clone the repo
git clone https://github.com/the-reticent/breede-berg-api.git
cd breede-berg-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-django-secret-key
DB_NAME=breede_berg
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Database Setup

```bash
# Create the database in PostgreSQL
createdb breede_berg

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/api/docs/` for the interactive Swagger documentation.

---

## Excel Import

Upload an `.xlsx` file to populate water quality readings in bulk:

```bash
curl -X POST http://localhost:8000/api/v1/import/water-quality/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@your_data.xlsx"
```

### Required Excel Columns

| Column | Required | Format |
|---|---|---|
| site_name | Yes | Must match an existing site name |
| recorded_at | Yes | YYYY-MM-DD or YYYY-MM-DD HH:MM:SS |
| ph | No | Decimal |
| dissolved_oxygen | No | Decimal (mg/L) |
| turbidity | No | Decimal (NTU) |
| temperature | No | Decimal (°C) |
| conductivity | No | Decimal (µS/cm) |
| notes | No | Text |

### Import Response

```json
{
    "message": "Import complete. 24 readings created.",
    "created": 24,
    "errors": [],
    "error_count": 0
}
```

---

## Authentication

Obtain a token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Use the token in subsequent requests:

```bash
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/v1/sites/
```

Read endpoints are public. Write endpoints (POST, PUT, PATCH, DELETE) require a valid token.

---

## Project Structure

```
breede-berg-api/
├── config/                 # Django settings and URL routing
├── sites/                  # Monitoring sites app
├── water_quality/          # Water quality readings + Excel importer
├── vegetation/             # Vegetation survey app
├── wildlife/               # Wildlife sightings app
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Background

This project was built at the intersection of two industries — telecommunications and environmental restoration. The data infrastructure gap in ecology is striking: while telecoms process terabytes of real-time data through robust pipelines, environmental scientists are still emailing spreadsheets.

The skills that optimise network performance transfer directly to biodiversity databases. REST APIs that connect global infrastructure can connect habitat monitoring systems. This project is proof of that.

---

## Roadmap

- [x] Seed data for real Breede and Berg river monitoring sites
- [ ] CSV importer for vegetation and wildlife data
- [ ] Date range filtering across all endpoints
- [ ] River health summary endpoint (aggregated statistics per site)
- [ ] Deployment to cloud (Railway / Render)
- [ ] Frontend dashboard for data visualisation

---

## License

MIT

---

## Author

**Kudakwashe Mike Mapaya**
Python Developer · Data Engineer · Environmental Tech

[LinkedIn](https://linkedin.com/in/kudakwashe-mike-mapaya-654281160) · [Email](mailto:kudamapaya@gmail.com)
