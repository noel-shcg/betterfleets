from django.db import migrations


def repair_livery_id_sequence(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT setval(
                pg_get_serial_sequence('"vehicles_livery"', 'id'),
                COALESCE(MAX(id), 1),
                MAX(id) IS NOT NULL
            )
            FROM vehicles_livery
            """
        )


class Migration(migrations.Migration):
    dependencies = [
        ("vehicles", "0103_drop_orphan_column_not_null"),
    ]

    operations = [
        migrations.RunPython(repair_livery_id_sequence, migrations.RunPython.noop),
    ]
