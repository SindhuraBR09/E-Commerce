# Generated by Django 3.2.3 on 2021-06-18 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Urbanity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='item_image',
        ),
    ]
