# Courier — Generic Django Zone-Based Shipping Cost Calculator

[![PyPI version](https://badge.fury.io/py/courier.svg)](https://pypi.org/project/courier/)
[![Python](https://img.shields.io/pypi/pyversions/courier.svg)](https://pypi.org/project/courier/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Author:** [Nitesh Kumar Singh](https://github.com/nkscoder) · **GitHub:** [@nkscoder](https://github.com/nkscoder)

A **generic, reusable Django courier app** for calculating zone-based shipping costs by weight, quantity, and destination. Works out of the box with built-in country/region models, or plugs into your existing location tables. Built by **Nitesh Kumar Singh (nkscoder)**.

> **Keywords:** django courier · generic shipping calculator · zone-based shipping · weight pricing · reusable django app · nkscoder · nitesh kumar singh · python shipping

---

## Features

- **Generic by design** — built-in `CourierCountry` / `CourierRegion` models, no `core` app required
- **Configurable pricing** — domestic multiplier, international surcharge %, weight units, thresholds
- **Zone-based pricing** — map countries and regions to shipping zones
- **Weight slab lookup** — automatic cost lookup by weight brackets
- **Multi-unit support** — grams, kilograms, and pounds (`gram`, `kgs`, `lbs`)
- **JSON API endpoint** — real-time shipping quotes via HTTP GET
- **Python API** — call `calculate_courier_cost()` from checkout, cart, or background jobs
- **Custom zone resolver** — plug in your own location models with one settings hook
- **Django Admin** — manage countries, regions, zones, and weight costs

---

## Requirements

- Python 3.8–3.12 (including **3.12**)
- Django 3.2+

---

## Installation

```bash
pip install courier
```

With Django Admin CSV import/export:

```bash
pip install "courier[admin]"
```

From GitHub:

```bash
pip install git+https://github.com/nkscoder/courier.git
```

---

## Quick start

```python
# settings.py
INSTALLED_APPS = [
    ...
    "courier",
]

COURIER_DOMESTIC_COUNTRY_NAME = "India"
COURIER_INTERNATIONAL_SURCHARGE_PERCENT = 22
```

```bash
python manage.py migrate courier
```

```python
# urls.py
urlpatterns = [
    path("courier/", include("courier.urls")),
]
```

---

## Usage

### Python API (recommended)

```python
from courier.calculator import calculate_courier_cost

total = calculate_courier_cost(
    weight=1.5,
    quantity=2,
    weight_unit="kgs",
    country_id=country.pk,
    region_id=region.pk,  # optional for domestic regions
)
```

Backward-compatible alias:

```python
from courier import courier_cost

total = courier_cost(weight=500, quantity=1, weight_unit="gram", country=1, state=3)
```

### HTTP API

```
GET /courier/?weight=500&quantity=2&weight_unit=gram&country=1&region=3
```

Response:

```json
{"total": 150}
```

| Parameter | Description |
|-----------|-------------|
| `weight` | Package weight |
| `quantity` | Number of packages |
| `weight_unit` | `gram`, `kgs`, or `lbs` |
| `country` | Country PK |
| `region` or `state` | Region PK (for domestic destinations) |

---

## Configuration

All settings use the `COURIER_` prefix:

| Setting | Default | Description |
|---------|---------|-------------|
| `COURIER_COUNTRY_MODEL` | `courier.CourierCountry` | Country model label |
| `COURIER_REGION_MODEL` | `courier.CourierRegion` | Region/state model label |
| `COURIER_DOMESTIC_COUNTRY_NAME` | `India` | Fallback domestic country name |
| `COURIER_INTERNATIONAL_SURCHARGE_PERCENT` | `22` | Surcharge for non-domestic destinations |
| `COURIER_HEAVY_WEIGHT_THRESHOLD_KG` | `20` | Heavy shipment threshold |
| `COURIER_WEIGHT_PADDING_KG` | `0.500` | Padding added to billable weight |
| `COURIER_WEIGHT_INCREMENT_KG` | `0.500` | Domestic weight multiplier increment |
| `COURIER_DEFAULT_WEIGHT_UNIT` | `gram` | Default unit for API requests |
| `COURIER_DOMESTIC_USE_WEIGHT_MULTIPLIER` | `True` | Per-increment pricing for domestic |
| `COURIER_ZONE_RESOLVER` | `None` | Custom `(country_id, region_id) -> (connection, surcharge)` |

### Plug into your own location models

```python
# settings.py
COURIER_COUNTRY_MODEL = "myapp.Country"
COURIER_REGION_MODEL = "myapp.State"

def resolve_courier_zone(country_id, region_id):
    from courier.models import ZoneConnection
    # your lookup logic
    return connection, apply_surcharge

COURIER_ZONE_RESOLVER = resolve_courier_zone
```

Mark domestic countries with `is_domestic=True` on your model, or rely on `COURIER_DOMESTIC_COUNTRY_NAME`.

---

## Admin setup

1. **Courier Country** — add destinations; mark domestic with `is_domestic`
2. **Courier Region** — add states/provinces under domestic countries
3. **Zone** — create shipping zones (Zone A, Zone B, …)
4. **Zone Connection** — link zones to countries and/or regions
5. **Weight Cost** — set price per weight slab for each zone

---

## How pricing works

1. Resolve the destination **zone** from country/region via `ZoneConnection`
2. Normalize weight to grams and compute total billable weight
3. Look up the matching **WeightCost** slab for that zone
4. **Domestic**: multiply slab rate by weight increments (configurable)
5. **International**: apply configurable **surcharge %** on the base rate

---

## Development

```bash
git clone git@github.com:nkscoder/courier.git
cd courier
pip install -e ".[admin]"
python manage.py migrate
python manage.py test courier
```

---

## Changelog

### 1.1.0
- Generic built-in `CourierCountry` / `CourierRegion` models (no `core` dependency)
- New `calculate_courier_cost()` service API
- Configurable settings via `COURIER_*` prefix
- Optional custom `COURIER_ZONE_RESOLVER` hook
- Improved admin with search and filters

### 1.0.0
- Initial PyPI release by **Nitesh Kumar Singh (nkscoder)**

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
