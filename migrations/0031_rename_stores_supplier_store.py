# Generated by Django 5.0 on 2024-08-06 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0030_salarychange_manager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='stores',
            new_name='store',
        ),
    ]
