# Generated by Django 4.2.3 on 2023-10-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_ticket_verification_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='id_verified',
            field=models.BooleanField(default=False),
        ),
    ]
