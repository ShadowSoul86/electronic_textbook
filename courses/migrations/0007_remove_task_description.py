# Generated by Django 4.2.3 on 2024-06-13 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_answer_answer_body_taskoption_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
    ]
