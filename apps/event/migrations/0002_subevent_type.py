# Generated by Django 4.2.3 on 2023-09-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subevent',
            name='type',
            field=models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], default='standard', max_length=100),
        ),
    ]