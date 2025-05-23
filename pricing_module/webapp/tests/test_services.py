from decimal import Decimal
from django.test import TestCase
from webapp.models import (
    PricingConfig,
    DistanceBasePrice,
    DistanceAdditionalPrice,
    TimeMultiplierFactor,
    WaitingCharge
)
from webapp.services import calculate_price
class CalculatePriceServiceTests(TestCase):
    def setUp(self):
        self.config = PricingConfig.objects.create(name="Config Test", is_active=True)

        DistanceBasePrice.objects.create(
            pricing_config=self.config,
            price=Decimal('80.00'),
            upto_km=Decimal('3.00'),
            days=["Wednesday"]
        )

        DistanceAdditionalPrice.objects.create(
            pricing_config=self.config,
            rate_per_km=Decimal('30.00'),
            applies_after_km=3.0
        )

        TimeMultiplierFactor.objects.create(
            pricing_config=self.config,
            start_min=60,
            end_min=120,
            multiplier=1.25
        )

        WaitingCharge.objects.create(
            pricing_config=self.config,
            free_minutes=3,
            charge_per_unit=Decimal('5.00'),
            unit_minutes=3
        )

    def test_calculate_price_normal_case(self):
        data = {
            "distance_km": 5.5,
            "total_minutes": 75,
            "waiting_minutes": 6,
            "day_of_week": "Wednesday"
        }
        result = calculate_price(data)

        self.assertEqual(result["base_price"], 80.0)
        self.assertEqual(result["extra_km"], 2.5)
        self.assertEqual(result["additional_km_charge"], 75.0)
        self.assertEqual(result["time_multiplier"], 1.25)
        self.assertEqual(result["waiting_charge"], 5.0)
        self.assertAlmostEqual(result["total"], 253.75, places=2)

    def test_calculate_price_missing_base_price(self):
        data = {
            "distance_km": 5.5,
            "total_minutes": 75,
            "waiting_minutes": 6,
            "day_of_week": "Monday"
        }
        with self.assertRaises(ValueError) as context:
            calculate_price(data)
        self.assertIn("No base price found", str(context.exception))

    def test_calculate_price_no_active_config(self):
        self.config.is_active = False
        self.config.save()
        data = {
            "distance_km": 5.5,
            "total_minutes": 75,
            "waiting_minutes": 6,
            "day_of_week": "Wednesday"
        }
        with self.assertRaises(ValueError) as context:
            calculate_price(data)
        self.assertIn("No active pricing config found", str(context.exception))
