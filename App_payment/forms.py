from django.forms import ModelForm
from .models import BillingAddress


class BillingAddressForm(ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ['user']
