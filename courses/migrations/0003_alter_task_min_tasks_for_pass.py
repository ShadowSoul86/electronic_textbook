# Generated by Django 4.2.3 on 2024-06-11 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_answer_status_answer_task_task_min_tasks_for_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='min_tasks_for_pass',
            field=models.IntegerField(default=0, verbose_name='Мин. Кол-во задач для прохождения'),
        ),
    ]
