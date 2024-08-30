# Generated by Django 5.0 on 2024-08-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adc', '0031_rename_stores_supplier_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='store',
        ),
        migrations.AddField(
            model_name='supplier',
            name='stores',
            field=models.ManyToManyField(related_name='suppliers', to='adc.store'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='suppliers/'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]