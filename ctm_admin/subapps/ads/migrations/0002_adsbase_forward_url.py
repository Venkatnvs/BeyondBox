# Generated by Django 4.2.7 on 2023-12-03 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsbase',
            name='forward_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
