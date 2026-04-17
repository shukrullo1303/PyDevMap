from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_submissionmodel_user_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonmodel',
            name='required_task',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='required_in_lessons',
                to='core.taskmodel',
            ),
        ),
    ]
