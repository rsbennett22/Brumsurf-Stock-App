# Generated by Django 4.0.6 on 2022-08-16 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='brand',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
