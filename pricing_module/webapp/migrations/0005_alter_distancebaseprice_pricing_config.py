# Generated by Django 4.2.21 on 2025-05-20 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_pricingconfig_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distancebaseprice',
            name='pricing_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_prices', to='webapp.pricingconfig'),
        ),
    ]
