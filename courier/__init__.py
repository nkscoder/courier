"""Django zone-based courier shipping calculator by Nitesh Kumar Singh (nkscoder)."""

__version__ = "1.1.1"
__author__ = "Nitesh Kumar Singh"
__author_handle__ = "nkscoder"

__all__ = ["__version__", "calculate_courier_cost", "courier_cost", "CourierCalculationError"]


def __getattr__(name):
    if name in {"calculate_courier_cost", "courier_cost", "CourierCalculationError"}:
        from .calculator import (
            CourierCalculationError,
            calculate_courier_cost,
            courier_cost,
        )

        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
