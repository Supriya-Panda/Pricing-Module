from decimal import Decimal
from .models import PricingConfig
import math

def calculate_price(data):
    distance = Decimal(str(data["distance_km"]))  
    time = Decimal(str(data["total_minutes"]))
    waiting = Decimal(str(data["waiting_minutes"]))
    day = data.get("day_of_week", "").strip()[:3].lower()     
    config = PricingConfig.objects.filter(is_active=True).first()
    if not config:
        raise ValueError("No active pricing config found.")

    dbp = config.base_prices.filter(days__icontains=day).first()
    if not dbp:
        raise ValueError(f"No base price found for day {day}.")
    base_price = dbp.price
    extra_km = max(Decimal('0'), distance - dbp.upto_km)

    dap = config.additional_prices.first()  
    additional_price = extra_km * dap.rate_per_km if dap else Decimal('0')

    multiplier = 1
    for tmf in config.time_multipliers.all():
        if tmf.start_min <= time <= tmf.end_min:
            multiplier = tmf.multiplier
            break

    wc = config.waiting_charges.first()
    waiting_charge = 0
    if wc and waiting > wc.free_minutes:
        extra_wait = waiting - wc.free_minutes
        
        chargeable_units = math.ceil(float(extra_wait) / float(wc.unit_minutes))
        waiting_charge = Decimal(chargeable_units) * wc.charge_per_unit
    else:
        waiting_charge = Decimal('0')
        
    time_charge = time * Decimal(str(multiplier))
    total = float(base_price + additional_price + time_charge + waiting_charge)

  
    return {
        "base_price": float(base_price),
        "extra_km": float(extra_km),
        "additional_km_charge": float(additional_price),
        "time_minutes": float(time),
        "time_multiplier": float(multiplier),
        "time_charge": float(time_charge),
        "waiting_minutes": float(waiting),
        "waiting_charge": float(waiting_charge),
        "total": float(total)
    }