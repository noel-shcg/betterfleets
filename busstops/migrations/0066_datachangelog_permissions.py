# Generated manually for permission changes

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busstops', '0065_service_colour_default'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datachangelog',
            options={
                'ordering': ('-created_at', '-id'),
                'permissions': [
                    ('approve_datachangelog', 'Can approve data change log'),
                    ('reject_datachangelog', 'Can reject data change log'),
                ],
                'indexes': [
                    ('busstops_data_status_target_model_idx', ['status', 'target_model']),
                    ('busstops_data_source_created_at_idx', ['source', 'created_at']),
                ],
            },
        ),
    ]
