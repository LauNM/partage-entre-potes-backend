# Generated by Django 3.2.5 on 2023-08-21 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_auto_20230821_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='is_active',
        ),
    ]
