from django.db import migrations


class Migration(migrations.Migration):
    """
    0002 already creates the TaskModel table via Django ORM.
    This migration is a no-op kept for migration history compatibility.
    """

    dependencies = [
        ("core", "0002_recreate_taskmodel_if_missing"),
    ]

    operations = []
