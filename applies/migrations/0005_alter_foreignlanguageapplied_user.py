# Generated by Django 4.2.7 on 2023-12-10 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applies', '0004_foreignlanguage_foreignlanguageapplied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreignlanguageapplied',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]