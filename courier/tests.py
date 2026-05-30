from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from courier.calculator import apply_pricing, normalize_weight


class NormalizeWeightTests(SimpleTestCase):
    def test_grams(self):
        self.assertEqual(normalize_weight(500, "gram"), Decimal("500"))

    def test_kgs(self):
        self.assertEqual(normalize_weight(1.5, "kgs"), Decimal("1500"))

    def test_lbs(self):
        self.assertEqual(normalize_weight(1, "lbs"), Decimal("453.592"))


@override_settings(
    COURIER_DOMESTIC_USE_WEIGHT_MULTIPLIER=True,
    COURIER_WEIGHT_INCREMENT_KG="0.500",
    COURIER_INTERNATIONAL_SURCHARGE_PERCENT=22,
)
class ApplyPricingTests(SimpleTestCase):
    def test_domestic_multiplier(self):
        cost = MagicMock()
        cost.amount = Decimal("10")
        amount = apply_pricing(
            Decimal("2.0"),
            cost,
            domestic_pricing=True,
            apply_surcharge=False,
        )
        self.assertEqual(amount, Decimal("40"))

    def test_international_surcharge(self):
        cost = MagicMock()
        cost.amount = Decimal("100")
        amount = apply_pricing(
            Decimal("1.0"),
            cost,
            domestic_pricing=False,
            apply_surcharge=True,
        )
        self.assertEqual(amount, Decimal("122"))
