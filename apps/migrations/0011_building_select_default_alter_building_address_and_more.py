# Generated by Django 5.0.3 on 2024-03-12 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_rename_users_client_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='select_default',
            field=models.CharField(choices=[('CustomInput', '--- Custom Input ---'), ('West Boca Executive Suites Building', 'West Boca Executive Suites Address'), ('7777 Glade Road Building', '7777 Glade Road Address')], default='CustomInput', max_length=500),
        ),
        migrations.AlterField(
            model_name='building',
            name='address',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
