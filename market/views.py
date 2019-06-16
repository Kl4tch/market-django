from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
from scraper.models import *
# from user.models import Comment, User
from user.views import main
from django.http import JsonResponse
from django.utils.timezone import now
import datetime
from scraper.models import StoreItem
from .forms import *
from django.db.models import Min
from django import template


# Create your views here.
def index(request):
    return render(request, 'market/index.html')


def test(request):
    return render(request, 'market/test/category.html')


def detail(request, slug, id):
    item = get_object_or_404(Item, id=id, slug=slug)
    images = Image.objects.filter(item__in=Item.objects.filter(id=id))

    attrs = ItemDetail.objects.filter(item=item)
    groups = GroupTitle.objects.all()
    storeItems = StoreItem.objects.filter(item=item)
    # comments = Comment.objects.filter(item=id).order_by('-date')

    # def _sort_comments(id):
    #     _sort_comments()



    context = {
        'item': item,
        'images': images,
        'attrs': attrs,
        'groups': groups,
        'storeItems': storeItems,
        # 'comments': comments,
        'var': None,
    }

    return render(request, 'market/detail.html', context)


# def add(request, slug, id):
#     selected = get_object_or_404(Item, id=id, slug=slug)
#
#     try:
#         token = request.session['access_token']
#         profile = User.objects.get(access_token=token)
#
#         Cart.objects.create(item=selected, user=profile, quantity=1)
#
#         context = {
#             'user': profile,
#         }
#
#         return redirect(main)
#
#     except:
#         return redirect('/')


def add_review(request, slug, id):

    if request.method == 'POST':
        dat = request.POST.get('text', None)
        return JsonResponse(dat)

    selected = get_object_or_404(Item, id=id, slug=slug)

    try:
        token = request.session['access_token']
        # profile = User.objects.get(access_token=token)

        # Comment.objects.create(item=selected, user=profile, rate='5', text="TESTrrrrrr")

    except:
        return redirect('/')


def products(request, category):
    itemsCategory = Item.objects.filter(category__in=Category.objects.filter(folder=category))
    imageItems = Image.objects.filter(item__in=itemsCategory, position=0)
    searchForm = SearchForm()

    brands = []

    for i in itemsCategory:
        brands.append(i.brand)

    brands_set = set(brands)
    unique_brands = (list(brands_set))

    itemsStores = StoreItem.objects.filter(item__in=itemsCategory)

    for item in itemsCategory:
        itemStores = itemsStores.filter(item=item)
        itemMinPrice = itemStores.annotate(min=Min('price'))
        item.priceRozetka = itemMinPrice[0].min


    filtersTitle = AttributeTitle.objects.all().filter(isFiltered=True)

    filterValues = ItemDetail.objects.all().filter(item__in=itemsCategory, attr__attributeTitle__isFiltered=True)

    filterValuesUnique = []

    for i in filterValues:
        for i2 in filterValuesUnique:
            if i.attr != i2.attr:
                filterValuesUnique.append(i)

    for i in filterValuesUnique:
        print(i)

    filterTitles = []

    for i in filterValues:
        filterTitles.append(i)

    filterTitles_set = set(filterTitles)
    unique_Titles = list(filterTitles_set)



    context = {
        'searchForm': searchForm,
        'all_items': itemsCategory,
        'all_images': imageItems,
        'category': category,
        'brands': unique_brands,
        'filterTitles': filtersTitle,
        'filterValues': filterValuesUnique,

    }

    return render(request, 'market/products.html', context)


def category(request):
    categories = get_list_or_404(Category)

    return render(request, 'market/categories.html', {'categories': categories})


def searchAll(request):
    search = request.GET.get('search')
    form = SearchAllForm(initial={'search': search})
    items = Item.objects.filter(title__contains=search).order_by('-date')

    imageItems = Image.objects.filter(item__in=items, position=0)

    context = {
        'search_all_form': form,
        'all_items': items,
        'all_images': imageItems,
    }

    return render(request, 'market/products.html', context)


def searchInCategory(request, category):
    print("HERE")
    searchTitle = request.GET.get('search')
    brands = request.GET.getlist('brand')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')

    print(brands)

    form = SearchForm(initial={'search': searchTitle})

    if brands != []:
        items = Item.objects.filter(title__contains=searchTitle, brand__name__in=brands,
                                category__in=Category.objects.filter(folder=category)).order_by('-date')
    else:
        items = Item.objects.filter(title__contains=searchTitle,
                                category__in=Category.objects.filter(folder=category)).order_by('-date')

    imageItems = Image.objects.filter(item__in=items, position=0)


    itemsStores = StoreItem.objects.filter(item__in=items)

    for item in items:
        itemStores = itemsStores.filter(item=item)
        itemMinPrice = itemStores.annotate(min=Min('price'))
        item.priceRozetka = itemMinPrice[0].min

    newItems = []
    for item in items:
        if minPrice != "" or maxPrice != "":
            if item.priceRozetka > int(minPrice) and item.priceRozetka < int(maxPrice):
                newItems.append(item)


    brands = []

    allItems = Item.objects.filter(category__in=Category.objects.filter(folder=category))

    for i in allItems:
        brands.append(i.brand)

    brands_set = set(brands)
    unique_brands = (list(brands_set))

    context = {
        'searchForm': form,
        'all_items': newItems,
        'all_images': imageItems,
        'brands': unique_brands,
    }

    return render(request, 'market/products.html', context)
