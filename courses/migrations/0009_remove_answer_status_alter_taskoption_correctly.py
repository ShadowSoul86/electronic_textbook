# Generated by Django 4.2.3 on 2024-06-16 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_taskoption_correctly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='status',
        ),
        migrations.AlterField(
            model_name='taskoption',
            name='correctly',
            field=models.BooleanField(default=False, verbose_name='Корректный ответ'),
        ),
    ]
