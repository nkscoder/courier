"""Configurable settings for the courier Django app — Nitesh Kumar Singh (nkscoder)."""

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULTS = {
    "AUTHOR_NAME": "Nitesh Kumar Singh",
    "AUTHOR_HANDLE": "nkscoder",
    "GITHUB_URL": "https://github.com/nkscoder/courier",
    "PYPI_URL": "https://pypi.org/project/nkscoder-courier/",
    "SEO_SITE_NAME": "Django Courier Shipping Calculator",
    "SEO_DESCRIPTION": (
        "Generic open-source Django courier and shipping cost calculator with "
        "zone-based weight pricing, domestic region zones, and international "
        "surcharge support. Built by Nitesh Kumar Singh (nkscoder)."
    ),
    "SEO_KEYWORDS": (
        "django courier, shipping cost calculator, zone-based shipping, "
        "weight-based courier pricing, generic django shipping, django shipping app, "
        "nkscoder, nitesh kumar singh, python courier, ecommerce shipping"
    ),
    # Location models (override to plug into your own Country/State tables)
    "COUNTRY_MODEL": "courier.CourierCountry",
    "REGION_MODEL": "courier.CourierRegion",
    # Pricing defaults
    "DOMESTIC_COUNTRY_NAME": "India",
    "INTERNATIONAL_SURCHARGE_PERCENT": 22,
    "HEAVY_WEIGHT_THRESHOLD_KG": 20,
    "WEIGHT_PADDING_KG": "0.500",
    "WEIGHT_INCREMENT_KG": "0.500",
    "DEFAULT_WEIGHT_UNIT": "gram",
    "SUPPORTED_WEIGHT_UNITS": ("gram", "kgs", "lbs"),
    "DOMESTIC_USE_WEIGHT_MULTIPLIER": True,
    # Optional hook: callable(country_id, region_id) -> (zone_connection, apply_surcharge)
    "ZONE_RESOLVER": None,
}


def get_setting(name):
    key = f"COURIER_{name}"
    if hasattr(settings, key):
        return getattr(settings, key)
    return DEFAULTS[name]


def get_model(label):
    try:
        return apps.get_model(label)
    except (LookupError, ValueError) as exc:
        raise ImproperlyConfigured(f"COURIER model {label!r} is not installed.") from exc


def get_country_model():
    return get_model(get_setting("COUNTRY_MODEL"))


def get_region_model():
    return get_model(get_setting("REGION_MODEL"))
