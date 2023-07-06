from django.db import models
from App_login.models import Sellar

# Create your models here.


class Catagory(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Catagories'


class Product(models.Model):
    catagory = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, related_name='product_catagory')

    sellar = models.ForeignKey(
        Sellar, on_delete=models.CASCADE, related_name='product_sellar')
    product_image = models.ImageField(upload_to='product_image')
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    short_text = models.CharField(max_length=40)
    product_description = models.TextField(verbose_name='product discription')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
