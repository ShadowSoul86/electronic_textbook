# Generated by Django 4.2.3 on 2024-06-16 21:53

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_task_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=courses.models.attachment_upload, verbose_name='Методический материал'),
        ),
    ]
