# Generated by Django 4.2.7 on 2024-01-17 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
