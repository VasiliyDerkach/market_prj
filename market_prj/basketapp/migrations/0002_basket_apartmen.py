# Generated by Django 3.0.3 on 2025-04-04 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_apartmen'),
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='apartmen',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Apartmen'),
        ),
    ]
