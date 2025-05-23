from django.contrib import admin
from .forms import PricingConfigForm
from .models import *

class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    extra = 1

class DistanceAdditionalPriceInline(admin.TabularInline):
    model = DistanceAdditionalPrice
    extra = 1

class TimeMultiplierFactorInline(admin.TabularInline):
    model = TimeMultiplierFactor
    extra = 1

class WaitingChargeInline(admin.TabularInline):
    model = WaitingCharge
    extra = 1


@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    inlines = [
        DistanceBasePriceInline,
        DistanceAdditionalPriceInline,
        TimeMultiplierFactorInline,
        WaitingChargeInline,
    ]
    list_display = ("name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        PricingConfigLog.objects.create(
            pricing_config=obj,
            changed_by=request.user,
            change_type="update" if change else "create",
            description=f"{'Updated' if change else 'Created'} config: {obj.name}",
        )