from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from App_login.models import Sellar
from App_shop.models import Product
from .forms import ProductForm

# Create your views here.


@login_required
def add_product(request):
    sellar = Sellar.objects.filter(user=request.user)[0]
    form = ProductForm()

    if sellar is not None and sellar.is_fully_filled():
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                add_product = form.save(commit=False)
                add_product.sellar = sellar
                add_product.save()
                messages.success(request, 'Product Added Successfully !')
    else:
        messages.success(request, 'Please fill up All Details')
        return HttpResponseRedirect(reverse('App_login:sellar'))

    return render(request, 'App_shop/add_product.html', context={'form': form})


def all_product(request):
    all_products = Product.objects.all().order_by('-create_at')

    return render(request, 'App_shop/home.html', context={'all_products': all_products})


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'App_shop/product_details.html', context={'product': product})


@login_required
def view_sellar_product(request):
    sellar = Sellar.objects.filter(user=request.user)
    if sellar.exists():
        products = Product.objects.filter(sellar=sellar[0])
        if not products.exists():
            messages.warning(request,'You Have No Product !')
            return HttpResponseRedirect(reverse('App_shop:home'))


    else:
        messages.warning(request, 'You Are Not Our Sellar !')
        return HttpResponseRedirect(reverse('App_shop:home'))

    return render(request, 'App_shop/sellar_product.html', context={'products':products})
