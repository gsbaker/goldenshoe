from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render
from django.template import loader

from shop.forms import SizeForm
from shop.models import Product


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def detail(request, product_id):
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            return HttpResponse('/')
    else:
        product = Product.objects.get(pk=product_id)
        form = SizeForm(initial={'product': product})

    product = Product.objects.get(pk=product_id)
    sizes = product.sizes.all()
    out_of_stock_sizes = []
    for size in sizes:
        if not size.in_stock:
            out_of_stock_sizes.append(str(size.number))


    context = {
        'product': Product.objects.get(pk=product_id),
        'form': form,
        'out_of_stock_sizes': out_of_stock_sizes,
    }
    return render(request, 'detail.html', context)
    # return render(request, 'detail.html', context)
