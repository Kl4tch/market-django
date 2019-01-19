from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *


# Create your views here.
def index(request):
    return render(request, 'market/index.html')


def test(request):
    return render(request, 'market/test/category.html')


def detail(request, iditem):
    item = get_object_or_404(Items, id=iditem)
    images = get_list_or_404(Image, item=iditem)

    return render(request, 'market/detail.html', {'item': item, 'images': images })


def products(request, category):
    all_items = Items.objects.filter(category__in=Category.objects.filter(folder=category))
    all_images = Image.objects.all()

    context = {'all_items': all_items, 'all_images': all_images}

    return render(request, 'market/products.html', context)


def category(request):
    categories = get_list_or_404(Category)

    return render(request, 'market/categories.html', {'categories': categories})
