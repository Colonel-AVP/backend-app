# Generated by Django 5.0.1 on 2024-01-24 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_subject_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='staff',
        ),
    ]
