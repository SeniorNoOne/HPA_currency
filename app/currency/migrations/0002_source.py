# Generated by Django 4.1.7 on 2023-03-03 13:36

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('source_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128,
                                                                         region=None, unique=True)),
            ],
        ),
    ]