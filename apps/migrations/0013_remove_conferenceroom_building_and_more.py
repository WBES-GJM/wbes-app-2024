# Generated by Django 5.0.3 on 2024-03-12 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_alter_building_select_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conferenceroom',
            name='building',
        ),
        migrations.AlterField(
            model_name='conferenceroom',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='conferenceroom',
            name='building',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.building'),
            preserve_default=False,
        ),
    ]
