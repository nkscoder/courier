from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from courier.views import get_amount


class GetAmountTests(SimpleTestCase):
    @patch("courier.views.WeightCost.objects")
    def test_india_weight_slabs(self, mock_weight_cost):
        cost = MagicMock()
        cost.amount = Decimal("10")
        mock_weight_cost.filter.return_value.filter.return_value.first.return_value = cost

        c_zone = MagicMock()
        c_zone.zone = MagicMock()
        c_zone.country.name = "India"

        amount = get_amount(2.0, c_zone, surcharge=False)
        self.assertEqual(amount, Decimal("40"))

    @patch("courier.views.WeightCost.objects")
    def test_international_surcharge(self, mock_weight_cost):
        cost = MagicMock()
        cost.amount = Decimal("100")
        mock_weight_cost.filter.return_value.filter.return_value.first.return_value = cost

        c_zone = MagicMock()
        c_zone.zone = MagicMock()
        c_zone.country.name = "United States"

        amount = get_amount(1.0, c_zone, surcharge=True)
        self.assertEqual(amount, Decimal("122"))
