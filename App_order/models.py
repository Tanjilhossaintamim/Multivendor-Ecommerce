from django.db import models
from django.contrib import messages
from django.conf import settings
from App_shop.models import Product

# Create your models here.


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expaired = models.BooleanField(default=False)
    discount = models.FloatField()
    min_amount = models.IntegerField(default=2000)

    def __str__(self):
        return self.coupon_code


class Cart(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_cart')

    item = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item.product_name} X {self.quantity}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_format = format(total, '0.2f')
        return float_format


class Order(models.Model):
    processing = 'processing'
    delivered = 'delivered'
    status_choices = [
        (processing, 'Processing'),
        (delivered, 'Delivered')
    ]
    order_items = models.ManyToManyField(Cart)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_coupon')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_order')
    ordered = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=status_choices, default=processing)

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():

            total += float(order_item.get_total())
        if self.coupon and self.coupon.is_expaired == False:
            if self.coupon.min_amount <= total:
                total = total - (total * (self.coupon.discount/100))
                return total

        return total
