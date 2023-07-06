# Generated by Django 4.2.3 on 2023-07-05 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_order', '0007_cart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('delivered', 'Delivered')], default=('processing', 'Processing'), max_length=10),
        ),
    ]