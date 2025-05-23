from django import forms
from .models import PricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

