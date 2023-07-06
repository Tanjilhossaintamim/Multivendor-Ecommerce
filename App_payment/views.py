from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from App_order.models import Order, Cart
from App_login.models import Profile
from .forms import BillingAddressForm
from .models import BillingAddress
from sslcommerz_lib import SSLCOMMERZ


# Create your views here.


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    address_form = BillingAddressForm(instance=saved_address[0])
    if request.method == 'POST':
        address_form = BillingAddressForm(
            data=request.POST, instance=saved_address[0])
        if address_form.is_valid():
            user_address_form = address_form.save(commit=False)
            user_address_form.user = request.user
            user_address_form.save()
            address_form = BillingAddressForm(instance=saved_address[0])
            messages.success(request, 'Address Saved Successfully !')
            return redirect('App_payment:checkout')

    return render(request, 'App_payment/checkout.html', context={'address_form': address_form, 'order_items': order_items, 'order_total': order_total})


@login_required
def payment(request):

    profile = Profile.objects.filter(user=request.user)[0]
    saved_address = BillingAddress.objects.filter(user=request.user)[0]

    if not profile.is_fully_filled():
        messages.warning(
            request, 'Please fill up all profile information first !')
        return redirect('App_login:profile')
    if not saved_address.is_fully_filled():
        messages.warning(request, 'Please fill up all  information first !')
        return redirect('App_payment:checkout')

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_total = order_qs[0].get_totals()
    order_count = order_qs[0].order_items.count()
    order_items = order_qs[0].order_items.all()

    store_id = 'ecomm648d7870e47c0'
    api_key = 'ecomm648d7870e47c0@ssl'

    settings = {'store_id': store_id, 'store_pass': api_key, 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)

    status_url = request.build_absolute_uri(reverse('App_payment:compleate'))
    current_user = request.user

    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = profile.fullname
    post_body['cus_email'] = current_user.email
    post_body['cus_phone'] = profile.phone
    post_body['cus_add1'] = profile.address
    post_body['cus_city'] = profile.city
    post_body['cus_country'] = profile.country
    post_body['shipping_method'] = "Curiar"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = order_count
    post_body['product_name'] = order_items
    post_body['product_category'] = "Mixed"
    post_body['product_profile'] = "general"

    post_body['ship_name'] = profile.fullname
    post_body['ship_add1'] = saved_address.address
    post_body['ship_city'] = saved_address.city
    post_body['ship_postcode'] = saved_address.zip_code
    post_body['ship_country'] = saved_address.country

    response = sslcommez.createSession(post_body)
    return redirect(response['GatewayPageURL'])


@csrf_exempt
def compleat(request):
    if request.method == 'POST' or request.method == 'post':
        response = request.POST
        status = response['status']
        if status == 'VALID':
            val_id = response['val_id']
            bank_tran_id = response['bank_tran_id']
            return HttpResponseRedirect(reverse('App_payment:purchased', kwargs={'tran_id': bank_tran_id, 'val_id': val_id}))

        elif status == 'FAILED':
            messages.error(request, 'Payment Failed !')
            return redirect('App_shop:home')

    return render(request, 'App_payment/compleate.html', context={})


@login_required
def purchased(request, tran_id, val_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.order_id = val_id
    order.payment_id = tran_id

    order.save()

    cart_item = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()
    messages.success(request, 'Payment Successfully Compleated !')
    return HttpResponseRedirect(reverse('App_shop:home'))


@login_required
def order(request):
    order_qs = Order.objects.filter(
        user=request.user, ordered=True)

    return render(request, 'App_payment/order.html', context={'order_items': order_qs})
