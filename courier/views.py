import json
from decimal import Decimal

from django.db.models import Q
from django.http import HttpResponse

from core.models import Country, State

from .models import WeightCost, ZoneConnection


def courier(request):
    """JSON endpoint: calculate shipping cost from query params."""
    weight = float(request.GET.get("weight", 0))
    quantity = int(request.GET.get("quantity", 1))
    weight_unit = request.GET.get("weight_unit", "gram")
    surcharge = False

    if weight_unit == "lbs":
        weight = weight * 453.592

    country = Country.objects.get(pk=request.GET.get("country"))
    if country.name == "India":
        state = State.objects.get(pk=request.GET.get("state"))
        c_zone = ZoneConnection.objects.filter(state=state.id).first()
    else:
        surcharge = True
        c_zone = ZoneConnection.objects.filter(country=country.id).first()

    t_weight = weight * quantity
    if t_weight > 20:
        f_weight = round((weight * quantity) + 0.500)
    else:
        f_weight = (weight * quantity) + 0.500

    total = round(get_amount(f_weight, c_zone, surcharge), 3)
    return HttpResponse(
        json.dumps({"total": int(total)}),
        content_type="application/json",
        status=200,
    )


def get_amount(weight, c_zone, surcharge):
    zone = c_zone.zone
    qst = Q(weight__lt=weight + 0.500) & Q(weight__gte=weight)
    cost = WeightCost.objects.filter(zone=zone).filter(qst).first()
    amount = 0
    if cost:
        if c_zone.country.name == "India":
            w_c = weight / 0.500
            amount = cost.amount * w_c
        else:
            amount = cost.amount
            if surcharge:
                amount = amount + (amount * 22 / 100)
    return amount


def courier_cost(weight, quantity, weight_unit, country, state):
    """Programmatic shipping cost calculator (grams/kg/lbs aware)."""
    surcharge = False

    if weight_unit == "lbs":
        weight = Decimal(weight) * Decimal("453.592")
    elif weight_unit == "kgs":
        weight = Decimal(weight) * Decimal("1000")
    elif weight_unit == "gram":
        weight = Decimal(weight)
    else:
        raise ValueError(f"Unknown weight unit: {weight_unit}")

    country_obj = Country.objects.get(pk=country)
    if country_obj.name.lower() == "india":
        state_obj = State.objects.get(pk=state)
        c_zone = ZoneConnection.objects.filter(state=state_obj.id).first()
    else:
        surcharge = True
        c_zone = ZoneConnection.objects.filter(country=country_obj.id).first()

    quantity = int(quantity)
    t_weight = weight * quantity
    t_weight_kg = t_weight / Decimal("1000")

    if t_weight_kg > 20:
        f_weight = round(t_weight_kg + Decimal("0.500"), 3)
    else:
        f_weight = t_weight_kg + Decimal("0.500")

    total = round(get_amount(float(f_weight), c_zone, surcharge), 3)
    return int(total)
