# Generated by Django 5.0.1 on 2024-01-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_company_alt_email_1_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
