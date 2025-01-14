# Generated by Django 5.0 on 2024-08-06 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0028_remove_billitem_bill_remove_billitem_article_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarychange',
            name='change_type',
            field=models.CharField(choices=[('raise', 'Raise'), ('deduction', 'Deduction')], default='raise', max_length=10),
        ),
        migrations.AlterField(
            model_name='salarychange',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
