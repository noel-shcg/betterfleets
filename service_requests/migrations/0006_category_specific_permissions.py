# Generated manually for category-specific permissions

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_requests', '0005_merge_20260919_2224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
                'permissions': [
                    ('approve_request', 'Can approve request'),
                    ('reject_request', 'Can reject request'),
                    ('change_request_status', 'Can change request status'),
                    ('approve_photo_request', 'Can approve photo request'),
                    ('approve_vehicle_request', 'Can approve vehicle request'),
                    ('approve_service_request', 'Can approve service request'),
                    ('approve_vehicle_type_request', 'Can approve vehicle type request'),
                    ('approve_operator_request', 'Can approve operator request'),
                ],
            },
        ),
    ]
