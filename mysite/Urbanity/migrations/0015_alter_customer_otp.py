# Generated by Django 3.2.3 on 2021-07-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Urbanity', '0014_customer_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='otp',
            field=models.IntegerField(null=True),
        ),
    ]
