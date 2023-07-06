from django.contrib import admin
from .models import Order, Cart, Coupon
# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''

    list_display = ('id', 'item', 'purchased', 'create_at', 'update_at')
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('id', 'ordered', 'order_id', 'payment_id', 'status','coupon')
    list_per_page = 10
    list_editable = ['status']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    '''Admin View for Coupon'''

    list_display = ('id', 'coupon_code', 'discount', 'min_amount','is_expaired')
    list_per_page = 10
