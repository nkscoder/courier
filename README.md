# Courier — Django Zone-Based Shipping Cost Calculator

[![PyPI version](https://badge.fury.io/py/courier.svg)](https://pypi.org/project/courier/)
[![Python](https://img.shields.io/pypi/pyversions/courier.svg)](https://pypi.org/project/courier/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Author:** [Nitesh Kumar Singh](https://github.com/nkscoder) · **GitHub:** [@nkscoder](https://github.com/nkscoder)

A reusable **Django courier app** for calculating zone-based shipping costs by weight, quantity, and destination. Built by **Nitesh Kumar Singh (nkscoder)** for e-commerce, logistics, and any Django project that needs flexible courier pricing.

> **Keywords:** django courier · shipping cost calculator · zone-based shipping · weight pricing · india courier zones · nkscoder · nitesh kumar singh · python shipping app

---

## Features

- **Zone-based pricing** — map countries and Indian states to shipping zones
- **Weight slab lookup** — automatic cost lookup by weight brackets
- **Multi-unit support** — grams, kilograms, and pounds (`gram`, `kgs`, `lbs`)
- **International surcharge** — optional 22% surcharge for non-India destinations
- **JSON API endpoint** — real-time shipping quotes via HTTP GET
- **Python API** — call `courier_cost()` directly from your checkout flow
- **Django Admin** — manage zones, connections, and weight costs (optional CSV import/export)

---

## Requirements

- Python 3.8+
- Django 3.2+
- A host project with a `core` app providing `Country` and `State` models

---

## Installation

### From PyPI (recommended)

```bash
pip install courier
```

### From GitHub

```bash
pip install git+https://github.com/nkscoder/courier.git
```

### With Django Admin import/export

```bash
pip install "courier[admin]"
```

---

## Setup

### Step 1 — Add to `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    "core",      # must provide Country and State models
    "courier",
]
```

### Step 2 — Run migrations

```bash
python manage.py migrate courier
```

### Step 3 — Configure zones in Django Admin

1. **Zone** — create shipping zones (e.g. Zone A, Zone B)
2. **Zone Connection** — link zones to countries and/or Indian states
3. **Weight Cost** — set price per weight slab for each zone

### Step 4 — Wire up URLs

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path("courier/", include("courier.urls")),
]
```

---

## Usage

### HTTP API

```
GET /courier/?weight=500&quantity=2&weight_unit=gram&country=1&state=3
```

Response:

```json
{"total": 150}
```

| Parameter | Description |
|-----------|-------------|
| `weight` | Package weight (number) |
| `quantity` | Number of packages |
| `weight_unit` | `gram`, `kgs`, or `lbs` |
| `country` | Country PK from your `core.Country` model |
| `state` | State PK (required for India) |

### Python API

```python
from courier.views import courier_cost

total = courier_cost(
    weight=1.5,
    quantity=1,
    weight_unit="kgs",
    country=country_id,
    state=state_id,
)
print(total)  # shipping cost as integer
```

---

## How pricing works

1. Resolve the destination **zone** from country/state via `ZoneConnection`
2. Convert weight to the correct unit and compute total weight
3. Look up the matching **WeightCost** slab for that zone
4. For India: multiply slab rate by weight increments (500 g units)
5. For international: apply a **22% surcharge** on top of the base rate

---

## Development

```bash
git clone git@github.com:nkscoder/courier.git
cd courier
pip install -e ".[admin]"
python manage.py migrate
python manage.py runserver
```

### Build & publish to PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

Or tag a release on GitHub — the included GitHub Action publishes automatically.

---

## Changelog

### 1.0.0
- PyPI packaging with `pyproject.toml`
- Code cleanup and modern Django app config
- SEO & documentation by **Nitesh Kumar Singh (nkscoder)**
- Optional `django-import-export` admin support

---

## Author & Links

| | |
|---|---|
| **Author** | Nitesh Kumar Singh |
| **GitHub** | [github.com/nkscoder](https://github.com/nkscoder) |
| **Repository** | [github.com/nkscoder/courier](https://github.com/nkscoder/courier) |
| **PyPI** | [pypi.org/project/courier](https://pypi.org/project/courier) |

---

## License

MIT License — Copyright (c) 2020-2026 [Nitesh Kumar Singh (nkscoder)](https://github.com/nkscoder)
