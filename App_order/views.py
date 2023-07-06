from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from App_shop.models import Product
from .models import Cart, Order, Coupon
from .forms import CouponForm

# Create your views here.


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    user_cart_item = Cart.objects.get_or_create(
        user=request.user, item=item, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            user_cart_item[0].quantity += 1
            user_cart_item[0].save()
            messages.info(request, 'Quantity was Updated !')
            return HttpResponseRedirect(reverse('App_shop:home'))
        else:
            order.order_items.add(user_cart_item[0])
            messages.info(
                request, 'This Product Successfully Added Your Cart !')
            return HttpResponseRedirect(reverse('App_shop:home'))
    else:
        order = Order(user=request.user, ordered=False)
        order.save()
        order.order_items.add(user_cart_item[0])
        messages.info(
            request, 'This Product Successfully Added Your Cart !')
        return HttpResponseRedirect(reverse('App_shop:home'))


@login_required
def cart(request):
    user_cart = Cart.objects.filter(user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    dic = {
        'user_cart': user_cart,



    }
    if order_qs.exists():
        if order_qs[0].coupon:
            dic.update({
                'allredy_coupon': True
            })
        else:
            dic.update({
                'allredy_coupon': False
            })

    coupon = Coupon.objects.all().order_by('-id')[0]
    if coupon.is_expaired == False:
        dic.update({
            'coupon': coupon
        })

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(
            coupon_code=coupon_code, is_expaired=False)
        if coupon_obj.exists():
            if order_qs[0].get_totals() < coupon_obj[0].min_amount:
                messages.warning(
                    request, f'Your Amount is Low You Have to Shoping up to {coupon_obj[0].min_amount} tk !')
            else:

                order = order_qs[0]
                if order.coupon:

                    messages.info(request, 'You Got Already Discount !')
                else:
                    order.coupon = coupon_obj[0]
                    order.save()
                    messages.success(request, 'Coupon applied Successfully !')
                    return HttpResponseRedirect(reverse('App_order:cart'))
        else:
            messages.warning(request, 'Invalid Coupon !')

    if user_cart.exists() and order_qs.exists():
        order = order_qs[0]
        dic.update({'order': order})
        return render(request, 'App_order/cart.html', context=dic)
    else:
        messages.warning(request, 'Cart Is Empty !')
        return redirect('App_shop:home')


@login_required
def increase_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            user_cart_item = Cart.objects.filter(
                user=request.user, item=item, purchased=False)[0]
            if user_cart_item.quantity >= 1:
                user_cart_item.quantity += 1
                user_cart_item.save()

                messages.info(request, 'Quantity Updated Successfully !')
                return HttpResponseRedirect(reverse('App_order:cart'))
        else:
            messages.warning(request, 'This Product Not in Your Cart')
            return redirect('App_order:cart')


@login_required
def decrease_quantity(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            user_cart_item = Cart.objects.filter(
                user=request.user, item=item, purchased=False)[0]
            if user_cart_item.quantity > 1:
                user_cart_item.quantity -= 1
                user_cart_item.save()
                messages.success(request, 'Quantity Decreased !')
                return redirect('App_order:cart')

            else:
                user_cart_item.delete()
                messages.info(request, 'This Product Removed From Your Cart !')
                return redirect('App_order:cart')


@login_required
def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            user_cart_item = Cart.objects.filter(
                user=request.user, item=item, purchased=False)[0]
            user_cart_item.delete()
            messages.success(request, 'This Product Remove From Your Cart !')
            return HttpResponseRedirect(reverse('App_order:cart'))
        else:
            messages.warning(request, 'This Product Not In Your Cart !')
            return redirect('App_order:cart')
    else:
        messages.warning(request, 'You Have No Active Order')
        return redirect('App_shop:home')
