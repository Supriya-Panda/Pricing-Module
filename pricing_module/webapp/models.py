from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

DAY_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class PricingConfig(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"


class DistanceBasePrice(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='base_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upto_km = models.DecimalField(max_digits=5, decimal_places=2)
    days = MultiSelectField(choices=DAY_CHOICES, max_length=100)

    def __str__(self):
        return f"{self.price} INR up to {self.upto_km}KM on {', '.join(self.days)}"


class DistanceAdditionalPrice(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='additional_prices')
    rate_per_km = models.DecimalField(max_digits=6, decimal_places=2)
    applies_after_km = models.DecimalField(max_digits=5, decimal_places=2, default=3.0)

    def __str__(self):
        return f"{self.rate_per_km} INR/KM after {self.applies_after_km}KM"


class TimeMultiplierFactor(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='time_multipliers')
    start_min = models.PositiveIntegerField()
    end_min = models.PositiveIntegerField()
    multiplier = models.FloatField()

    def __str__(self):
        return f"{self.multiplier}x from {self.start_min} to {self.end_min} mins"


class WaitingCharge(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='waiting_charges')
    free_minutes = models.PositiveIntegerField(default=3)
    charge_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    unit_minutes = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.charge_per_unit} INR per {self.unit_minutes} min after {self.free_minutes} min"


class PricingConfigLog(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_type = models.CharField(max_length=10, choices=
        [
            ('create', 'Create'),
            ('update', 'Update'),
            ('delete', 'Delete')
        ])
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.change_type.title()} by {self.changed_by or 'Unknown'} at {self.timestamp}"
