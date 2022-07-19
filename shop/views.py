import decimal

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.template import loader

from shop.forms import SizeForm, PromoCodeForm
from shop.models import Product, BasketItem, PromoCode


def navigation(request):
    template = loader.get_template('navigation.html')
    return template.render()


def index(request):
    template = loader.get_template('index.html')
    products = Product.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'index.html', context)


def profile(request):
    return render(request, template_name='profile.html')


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = SizeForm(request.POST, initial={'product': product})
        if form.is_valid():
            selected_size = form.cleaned_data['sizes']
            new_basket_item = BasketItem()
            new_basket_item.product = product
            new_basket_item.size = selected_size
            flag = False
            for basket_item in BasketItem.objects.all():
                if new_basket_item.product == basket_item.product and new_basket_item.size == basket_item.size:
                    basket_item.qty += 1
                    basket_item.save()
                    flag = True
            if not flag:
                new_basket_item.save()
            # return HttpResponse('/')
    else:
        form = SizeForm(initial={'product': product})
    sizes = product.sizes.all()
    out_of_stock_sizes = []
    for size in sizes:
        if not size.in_stock:
            out_of_stock_sizes.append(str(size.number))
    context = {
        'product': product,
        'form': form,
        'out_of_stock_sizes': out_of_stock_sizes,
    }
    return render(request, 'detail.html', context)


def men(request):
    products = Product.objects.filter(gender='M')
    context = {
        'products': products,
        'gender': 'Men',
    }
    return render(request, 'products.html', context)


def women(request):
    products = Product.objects.filter(gender='F')
    context = {
        'products': products,
        'gender': 'Women',
    }
    return render(request, 'products.html', context)


def basket(request):
    basket_items = BasketItem.objects.all()
    total = 0

    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            activate_promo_code(request, code)
            form = PromoCodeForm()
    else:
        form = PromoCodeForm()

    # work out basket total
    for basket_item in basket_items:
        basket_item.price = basket_item.product.price
        basket_item.price *= basket_item.qty
        total += basket_item.price

    # find and apply active promo code (if one exists)
    active_promo_code = False
    promo_codes = PromoCode.objects.all()
    for promo_code in promo_codes:
        if promo_code.active:
            active_promo_code = True
            if promo_code.discount_type == '%':
                percent_change = 1 - (promo_code.discount_amount * 0.01)
                for basket_item in basket_items:
                    basket_item.discount_price = round(
                        basket_item.price * decimal.Decimal(float(percent_change)), 2
                    )
                    basket_item.save()
            elif promo_code.discount_type == '-':
                for basket_item in basket_items:
                    basket_item.discount_price = basket_item.price - promo_code.discount_amount

    if active_promo_code:
        discount_total = 0
        for basket_item in basket_items:
            discount_total += basket_item.discount_price
    else:
        discount_total = total
        for basket_item in basket_items:
            basket_item.discount_price = basket_item.price

    context = {
        'basket_items': basket_items,
        'total': total,
        'discount_total': discount_total,
        'request': request,
        'form': form,
    }
    return render(request, 'basket.html', context)


def activate_promo_code(request, promo_input):
    promo_codes = PromoCode.objects.all()

    # deactivate any active codes
    for promo_code in promo_codes:
        if promo_code.active:
            promo_code.active = False
            promo_code.save()

    # active promo_input (if exists)
    for promo_code in promo_codes:
        if promo_code.code == promo_input:
            promo_code.active = True
            promo_code.save()
            return redirect('shop:basket')

    return redirect('shop:basket')


def basket_item_delete(request, basket_item_id):
    basket_item = BasketItem.objects.get(pk=basket_item_id)
    basket_item.delete()
    return redirect('shop:basket')


def increment_basket_item(request, basket_item_id):
    basket_item = BasketItem.objects.get(pk=basket_item_id)
    basket_item.qty += 1
    basket_item.save()
    return redirect('shop:basket')


def decrease_basket_item(request, basket_item_id):
    basket_item = BasketItem.objects.get(pk=basket_item_id)
    basket_item.qty -= 1
    basket_item.save()
    return redirect('shop:basket')
