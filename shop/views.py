from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from shop.forms import SizeForm
from shop.models import Product, ProductSize, BasketItem


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = SizeForm(request.POST, initial={'product': product})
        if form.is_valid():
            selected_size = form.cleaned_data['sizes']
            basket_item = BasketItem()
            basket_item.product = product
            basket_item.size = selected_size
            basket_item.save()
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
    context = {
        'basket_items': basket_items,
    }
    return HttpResponse(template.render(context))
