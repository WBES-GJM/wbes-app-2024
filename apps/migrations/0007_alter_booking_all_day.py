# Generated by Django 5.0.3 on 2024-03-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_booking_all_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='all_day',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
