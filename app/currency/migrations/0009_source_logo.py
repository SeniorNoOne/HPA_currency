# Generated by Django 4.1.7 on 2023-04-16 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0008_alter_rate_options_rename_source_url_source_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]