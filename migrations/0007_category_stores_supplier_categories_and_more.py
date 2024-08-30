# Generated by Django 5.0 on 2024-07-16 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0006_remove_category_store_product_delete_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='stores',
            field=models.ManyToManyField(blank=True, related_name='categories', to='adc.store'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='adc.category'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='adc.product'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='stores',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='adc.store'),
        ),
    ]