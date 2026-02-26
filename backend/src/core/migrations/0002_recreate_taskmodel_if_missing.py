from django.db import migrations


def recreate_taskmodel(apps, schema_editor):
    TaskModel = apps.get_model("core", "TaskModel")
    try:
        # This will create the table if it does not exist.
        # If the table already exists, the backend will raise an error, which we ignore.
        schema_editor.create_model(TaskModel)
    except Exception:
        # Table probably already exists in this database; nothing to do.
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(recreate_taskmodel, reverse_code=migrations.RunPython.noop),
    ]
