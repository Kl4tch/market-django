from django.shortcuts import render
from .models import Items


# Create your views here.
def index(request):
    return render(request, 'market/index.html')


def products(request):
    all_items = Items.objects.all()

    context = {'all_items': all_items, }

    return render(request, 'market/products.html', context)
