from django.contrib import admin
from .models import Product, Catagory
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('id', 'product_name', 'price', 'old_price',
                    'product_image', 'short_text', 'create_at')

    list_per_page = 10


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
