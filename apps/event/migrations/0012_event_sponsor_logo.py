# Generated by Django 4.2.3 on 2023-10-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_alter_subevent_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsor_logo',
            field=models.ImageField(blank=True, upload_to='event'),
        ),
    ]