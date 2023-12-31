# Generated by Django 4.1.7 on 2023-10-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_client_starting_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='paid_base_amount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paymentplan',
            name='paid_interest',
            field=models.BooleanField(default=False),
        ),
    ]
