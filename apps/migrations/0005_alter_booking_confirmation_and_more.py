# Generated by Django 5.0.1 on 2024-02-05 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_rename_name_booking_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='confirmation',
            field=models.CharField(blank=True, default='CONFIRMATION_NOT_REAL', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_datetime',
            field=models.DateTimeField(blank=True),
        ),
    ]