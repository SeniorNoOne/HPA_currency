# Generated by Django 4.1.7 on 2023-03-03 13:44

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='city',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='source',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default='',
                                                                 max_length=128, region=None,
                                                                 unique=True),
        ),
    ]