# Generated by Django 5.0.3 on 2024-03-11 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_alter_booking_all_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='all_day',
        ),
    ]
