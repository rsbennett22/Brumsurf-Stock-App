# Generated by Django 4.0.6 on 2022-07-22 07:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_stockitem_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='number',
            field=models.PositiveBigIntegerField(default=0, unique=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]