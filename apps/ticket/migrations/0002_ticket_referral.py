# Generated by Django 4.2.3 on 2023-08-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='referral',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
