# Generated by Django 4.1.7 on 2023-10-29 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_paymentplan_date_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentplan',
            name='date_paid',
            field=models.DateField(),
        ),
    ]