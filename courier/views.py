import json

from django.http import HttpResponse, JsonResponse

from .calculator import CourierCalculationError, calculate_courier_cost
from .conf import get_setting


def courier(request):
    """JSON endpoint: calculate shipping cost from query params."""
    try:
        total = calculate_courier_cost(
            weight=request.GET.get("weight", 0),
            quantity=request.GET.get("quantity", 1),
            weight_unit=request.GET.get("weight_unit") or get_setting("DEFAULT_WEIGHT_UNIT"),
            country_id=request.GET.get("country"),
            region_id=request.GET.get("state") or request.GET.get("region"),
        )
    except CourierCalculationError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return HttpResponse(
        json.dumps({"total": total}),
        content_type="application/json",
        status=200,
    )
