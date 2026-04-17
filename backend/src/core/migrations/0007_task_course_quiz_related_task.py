from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_lesson_required_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='course',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='tasks',
                to='core.coursemodel',
            ),
        ),
        migrations.AddField(
            model_name='quizmodel',
            name='related_task',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='quizzes',
                to='core.taskmodel',
            ),
        ),
    ]
