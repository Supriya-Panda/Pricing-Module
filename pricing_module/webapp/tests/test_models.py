from decimal import Decimal
from django.test import TestCase
from webapp.models import PricingConfig, DistanceBasePrice, WaitingCharge
class ModelStringRepresentationTests(TestCase):
    def test_distance_base_price_str(self):
        config = PricingConfig.objects.create(name="CFG", is_active=False)
        dbp = DistanceBasePrice.objects.create(
            pricing_config=config,
            price=Decimal('50.00'),
            upto_km=Decimal('2.00'),
            days=['Monday','Tuesday']
        )
        self.assertIn('50.00', str(dbp))
        self.assertIn('2.00KM', str(dbp))
        self.assertIn('Monday', str(dbp))

    def test_waiting_charge_str(self):
        config = PricingConfig.objects.create(name="CFG2", is_active=False)
        wc = WaitingCharge.objects.create(
            pricing_config=config,
            free_minutes=2,
            charge_per_unit=Decimal('4.00'),
            unit_minutes=2
        )
        self.assertIn('4.00', str(wc))
        self.assertIn('2 min', str(wc))
