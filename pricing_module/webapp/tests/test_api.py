from decimal import Decimal
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from webapp.models import (
    PricingConfig,
    DistanceBasePrice,
    DistanceAdditionalPrice,
    TimeMultiplierFactor,
    WaitingCharge,
)

class PricingModuleAPITests(TestCase):
    def setUp(self):
        self.config = PricingConfig.objects.create(
            name="Test Config",
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_config=self.config,
            price=Decimal('80.00'),
            upto_km=Decimal('3.00'),
            days=['Wednesday']
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

        self.client = APIClient()
        self.url = reverse('calculate-price')  

    def test_price_calculation_endpoint_success(self):
        payload = {
            'distance_km': 5.5,
            'total_minutes': 75,
            'waiting_minutes': 6,
            'day_of_week': 'Wednesday'
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        expected_keys = [
            'base_price', 'extra_km', 'additional_km_charge',
            'time_minutes', 'time_multiplier', 'time_charge',
            'waiting_minutes', 'waiting_charge', 'total'
        ]
        for key in expected_keys:
            self.assertIn(key, data)
        self.assertAlmostEqual(data['base_price'], 80.00)
        self.assertAlmostEqual(data['extra_km'], 2.5)
        self.assertAlmostEqual(data['additional_km_charge'], 75.00)
        self.assertAlmostEqual(data['time_multiplier'], 1.25)
        self.assertAlmostEqual(data['waiting_charge'], 5.00)
        self.assertAlmostEqual(data['total'], 253.75, places=2)

    def test_price_calculation_missing_config(self):
        self.config.is_active = False
        self.config.save()
        payload = {
            'distance_km': 1,
            'total_minutes': 10,
            'waiting_minutes': 0,
            'day_of_week': 'Monday'
        }
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

