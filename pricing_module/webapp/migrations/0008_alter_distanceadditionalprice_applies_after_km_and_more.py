# Generated by Django 4.2.21 on 2025-05-21 07:55

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_distanceadditionalprice_pricing_config_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distanceadditionalprice',
            name='applies_after_km',
            field=models.DecimalField(decimal_places=2, default=3.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='distancebaseprice',
            name='days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=100),
        ),
    ]
