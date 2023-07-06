from django.contrib import admin
from .models import BillingAddress
# Register your models here.


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    '''Admin View for BillingAddress'''

    list_display = ('id', 'user', 'address', 'zip_code', 'city', 'country')
    list_per_page = 10
