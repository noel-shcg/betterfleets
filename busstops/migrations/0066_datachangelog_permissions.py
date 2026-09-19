# Generated manually for permission changes

from django.db import migrations, models


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
            },
        ),
    ]
