# Generated migration to add FLOAT field type to AdvancedField and update length field

from django.db import migrations, models


def update_length_field_type(apps, schema_editor):
    AdvancedField = apps.get_model('vehicles', 'AdvancedField')
    AdvancedField.objects.filter(slug='length').update(field_type='float')


def revert_length_field_type(apps, schema_editor):
    AdvancedField = apps.get_model('vehicles', 'AdvancedField')
    AdvancedField.objects.filter(slug='length').update(field_type='number')


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0101_add_emissions_advanced_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advancedfield',
            name='field_type',
            field=models.CharField(
                choices=[
                    ('boolean', 'Boolean (true/false)'),
                    ('number', 'Number'),
                    ('float', 'Float (decimal)'),
                    ('text', 'Text'),
                    ('date', 'Date'),
                    ('url', 'URL')
                ],
                default='text',
                max_length=20
            ),
        ),
        migrations.RunPython(update_length_field_type, revert_length_field_type),
    ]
