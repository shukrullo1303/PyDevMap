from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_supportmessage_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonmodel',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='lessons/videos/'),
        ),
    ]
