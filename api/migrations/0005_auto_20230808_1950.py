# Generated by Django 3.2.5 on 2023-08-08 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20230808_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
        migrations.DeleteModel(
            name='Friend_Request',
        ),
    ]
