"""Generic courier pricing logic — usable from views, checkout, or Celery tasks."""

from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Q

from .conf import get_country_model, get_region_model, get_setting
from .models import WeightCost, ZoneConnection

GRAMS_PER_LB = Decimal("453.592")
GRAMS_PER_KG = Decimal("1000")


class CourierCalculationError(Exception):
    """Raised when shipping cost cannot be calculated."""


def normalize_weight(weight, weight_unit):
    unit = (weight_unit or get_setting("DEFAULT_WEIGHT_UNIT")).lower()
    supported = get_setting("SUPPORTED_WEIGHT_UNITS")
    if unit not in supported:
        raise CourierCalculationError(
            f"Unknown weight unit {weight_unit!r}. Supported: {', '.join(supported)}"
        )

    value = Decimal(str(weight))
    if unit == "lbs":
        return value * GRAMS_PER_LB
    if unit == "kgs":
        return value * GRAMS_PER_KG
    return value


def is_domestic_country(country):
    if hasattr(country, "is_domestic"):
        return bool(country.is_domestic)
    return country.name.lower() == get_setting("DOMESTIC_COUNTRY_NAME").lower()


def resolve_zone_connection(country_id, region_id=None):
    custom = get_setting("ZONE_RESOLVER")
    if custom:
        return custom(country_id, region_id)

    country_model = get_country_model()
    country = country_model.objects.get(pk=country_id)
    domestic = is_domestic_country(country)

    if domestic and region_id:
        region_model = get_region_model()
        region = region_model.objects.get(pk=region_id)
        connection = ZoneConnection.objects.filter(regions=region).first()
        if connection:
            return connection, False

    connection = ZoneConnection.objects.filter(countries=country).first()
    if not connection:
        raise CourierCalculationError(
            f"No shipping zone configured for country id={country_id}."
        )
    return connection, not domestic


def billable_weight_kg(total_weight_grams):
    threshold = Decimal(str(get_setting("HEAVY_WEIGHT_THRESHOLD_KG")))
    padding = Decimal(str(get_setting("WEIGHT_PADDING_KG")))
    total_kg = total_weight_grams / GRAMS_PER_KG

    if total_kg > threshold:
        return total_kg + padding
    return total_kg + padding


def lookup_weight_cost(zone, weight_kg):
    increment = Decimal(str(get_setting("WEIGHT_INCREMENT_KG")))
    qst = Q(weight__lt=weight_kg + increment) & Q(weight__gte=weight_kg)
    return WeightCost.objects.filter(zone=zone).filter(qst).first()


def apply_pricing(weight_kg, cost, *, domestic_pricing, apply_surcharge):
    amount = Decimal("0")
    if not cost:
        return amount

    if domestic_pricing and get_setting("DOMESTIC_USE_WEIGHT_MULTIPLIER"):
        increment = Decimal(str(get_setting("WEIGHT_INCREMENT_KG")))
        multiplier = Decimal(str(weight_kg)) / increment
        amount = cost.amount * multiplier
    else:
        amount = cost.amount
        if apply_surcharge:
            percent = Decimal(str(get_setting("INTERNATIONAL_SURCHARGE_PERCENT")))
            amount = amount + (amount * percent / Decimal("100"))
    return amount


def calculate_courier_cost(
    *,
    weight,
    quantity=1,
    weight_unit=None,
    country_id,
    region_id=None,
):
    """
    Generic shipping cost calculator.

    Returns integer total (rounded) for the given destination and weight.
    """
    grams = normalize_weight(weight, weight_unit or get_setting("DEFAULT_WEIGHT_UNIT"))
    quantity = int(quantity)
    if quantity < 1:
        raise CourierCalculationError("Quantity must be at least 1.")

    connection, apply_surcharge = resolve_zone_connection(country_id, region_id)
    domestic_pricing = not apply_surcharge
    weight_kg = billable_weight_kg(grams * quantity)
    cost = lookup_weight_cost(connection.zone, weight_kg)
    total = apply_pricing(
        weight_kg,
        cost,
        domestic_pricing=domestic_pricing,
        apply_surcharge=apply_surcharge,
    )
    return int(total.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def courier_cost(weight, quantity, weight_unit, country, state=None):
    """Backward-compatible alias used by existing integrations."""
    return calculate_courier_cost(
        weight=weight,
        quantity=quantity,
        weight_unit=weight_unit,
        country_id=country,
        region_id=state,
    )
