# Generated by Django 4.2.3 on 2023-07-04 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_shop', '0001_initial'),
        ('App_order', '0002_rename_purshed_cart_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App_shop.product'),
        ),
    ]