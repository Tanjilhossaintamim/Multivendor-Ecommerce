# Generated by Django 4.2.3 on 2023-07-04 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
