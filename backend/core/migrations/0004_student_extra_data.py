# Generated by Django 5.0.1 on 2024-01-25 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_subject_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='extra_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
