# Generated manually for permission changes

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0098_merge_0050_advanced_field_0097_vehicle_advanced'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehiclerevision',
            options={
                'app_label': 'vehicles',
                'permissions': [
                    ('approve_vehiclerevision', 'Can approve vehicle revision'),
                ],
            },
        ),
    ]
