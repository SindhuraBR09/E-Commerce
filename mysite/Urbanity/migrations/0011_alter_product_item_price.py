# Generated by Django 3.2.3 on 2021-06-23 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Urbanity', '0010_auto_20210620_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
