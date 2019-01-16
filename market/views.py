from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.
def index(request):
    return render(request, 'market/index.html')


def test(request):
    return render(request, 'market/category.html')


def detail(request, iditem):
    item = get_object_or_404(Items, id=iditem)

    return render(request, 'market/detail.html', {'item': item })


def products(request):
    all_items = Items.objects.all()
    all_images = Image.objects.all()

    context = {'all_items': all_items, 'all_images': all_images}

    return render(request, 'market/products.html', context)
