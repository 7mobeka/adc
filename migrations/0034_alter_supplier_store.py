# Generated by Django 5.0 on 2024-08-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0033_rename_stores_supplier_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='store',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='adc.store'),
        ),
    ]
