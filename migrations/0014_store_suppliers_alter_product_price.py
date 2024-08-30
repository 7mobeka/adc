# Generated by Django 5.0 on 2024-07-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0013_remove_customertransaction_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='suppliers',
            field=models.ManyToManyField(blank=True, related_name='stores', to='adc.supplier'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]