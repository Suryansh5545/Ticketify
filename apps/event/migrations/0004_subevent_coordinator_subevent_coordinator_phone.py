# Generated by Django 4.2.3 on 2023-09-17 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_payment_gateway'),
    ]

    operations = [
        migrations.AddField(
            model_name='subevent',
            name='coordinator',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='subevent',
            name='coordinator_phone',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
