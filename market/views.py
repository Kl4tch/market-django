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
import operator



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
    # получаем все атрибуты поиска
    searchTitle = request.GET.get('search')
    brands = request.GET.getlist('brand')
    filterValues = request.GET.getlist('filterValue')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')

    searchForm = SearchForm(initial={'search': searchTitle})

    allItemsInCategory = Item.objects.filter(category__in=Category.objects.filter(folder=category)).order_by('-date')

    if filterValues != []:
        filters = []

        for i in filterValues:
            filters.append(AttributeValue.objects.get(id=i))

        a = ItemDetail.objects.filter(attr__in=filters)

        items = []

        for i in a:
            items.append(i.item)
    else:
        items = allItemsInCategory

    if searchTitle is not None and searchTitle != "":
        items = items.filter(title__contains=searchTitle)

    if brands != []:
        items = items.filter(brand__name__in=brands)

    def setPrices():
        itemsStores = StoreItem.objects.filter(item__in=items)

        for item in items:
            itemStores = itemsStores.filter(item=item)
            itemMinPrice = itemStores.annotate(min=Min('price'))
            item.priceRozetka = itemMinPrice[0].min

    setPrices()

    if (minPrice != "" and maxPrice != "") and (minPrice is not None and maxPrice is not None):
        newItems = []
        for item in items:
            if item.priceRozetka > int(minPrice) and item.priceRozetka < int(maxPrice):
                newItems.append(item)

        items = newItems


    imageItems = Image.objects.filter(item__in=items, position=0)

    def getUniqueBrands():
        brands = []

        for i in allItemsInCategory:
            brands.append(i.brand)

        brands_set = set(brands)
        return list(brands_set)

    setPrices()

    uniqueBrands = sorted(getUniqueBrands(), key=operator.attrgetter('name'))


    #--------------- вывод фильтров начало----------------------

    filterValues = ItemDetail.objects.all().filter(item__in=allItemsInCategory, attr__attributeTitle__isFiltered=True)
    filterValuesUnique = []
    testUniq = []

    for i in filterValues:
        if i.attr not in testUniq:
            testUniq.append(i.attr)
            filterValuesUnique.append(i.attr)

    filterValuesUnique = sorted(filterValuesUnique, key=operator.attrgetter('value'))

    filterTitles = []

    for i in filterValues:
        filterTitles.append(i.attr.attributeTitle)

    filterTitles_set = set(filterTitles)
    unique_Titles = list(filterTitles_set)

    # --------------- вывод фильтров конец----------------------

    context = {
        'searchForm': searchForm,
        'all_items': items,
        'all_images': imageItems,
        'category': category,
        'brands': uniqueBrands,
        'filterTitles': unique_Titles,
        'filterValues': filterValuesUnique,
    }

    return render(request, 'market/products.html', context)


def category(request):
    categories = get_list_or_404(Category)

    return render(request, 'market/categories.html', {'categories': categories})


def feedback(request):
    form = FeedBackForm()

    context = {
        'form': form,
    }

    return render(request, 'market/feedback.html', context)


def about(request):
    return render(request, 'market/about.html')


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
