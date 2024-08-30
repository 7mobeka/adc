# Generated by Django 5.0 on 2024-07-16 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0008_customertransaction_suppliertransaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='stores',
            field=models.ManyToManyField(blank=True, related_name='customers', to='adc.store'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='adc.store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='adc.store'),
        ),
    ]
