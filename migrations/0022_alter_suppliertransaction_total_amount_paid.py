# Generated by Django 5.0 on 2024-07-24 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0021_suppliertransaction_bill_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertransaction',
            name='total_amount_paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
