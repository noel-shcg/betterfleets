# Generated manually for permission changes

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_requests', '0002_request_historical'),
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
                ],
            },
        ),
    ]
