# Generated by Django 3.2.5 on 2023-08-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_surname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
