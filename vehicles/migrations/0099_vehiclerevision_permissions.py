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
                    ('change_vehiclerevision', 'Can change vehicle revision'),
                ],
                'constraints': [
                    {'fields': ['vehicle', 'to_operator'], 'name': 'unique_pending_operator', 'condition': {'pending': True}},
                    {'fields': ['vehicle', 'to_operated_by'], 'name': 'unique_pending_operated_by', 'condition': {'pending': True}},
                    {'fields': ['vehicle', 'to_type'], 'name': 'unique_pending_type', 'condition': {'pending': True}},
                    {'fields': ['vehicle', 'to_livery'], 'name': 'unique_pending_livery', 'condition': {'pending': True}},
                    {'fields': ['vehicle', 'to_garage'], 'name': 'unique_pending_garage', 'condition': {'pending': True}},
                ],
            },
        ),
    ]
