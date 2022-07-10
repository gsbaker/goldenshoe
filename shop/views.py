from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.template import loader

from shop.forms import SizeForm
from shop.models import Product, BasketItem


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


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
    # return render(request, 'detail.html', context)


def basket(request):
    template = loader.get_template('basket.html')
    basket_items = BasketItem.objects.all()
    total = 0

    for basket_item in basket_items:
        basket_item.price = basket_item.product.price
        basket_item.price *= basket_item.qty
        total += basket_item.price

    context = {
        'basket_items': basket_items,
        'total': total,
        'request': request,
    }
    return HttpResponse(template.render(context))


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
