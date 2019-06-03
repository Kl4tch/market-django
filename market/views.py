from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
# from user.models import Comment, User
from user.views import main
from django.http import JsonResponse
from django.utils.timezone import now
import datetime




# Create your views here.
def index(request):
    return render(request, 'market/index.html')


def test(request):
    return render(request, 'market/test/category.html')


def detail(request, slug, id):
    item = get_object_or_404(Item, id=id, slug=slug)
    images = Image.objects.filter(item__in=Item.objects.filter(id=id))

    attrs = ItemDetail.objects.filter(item=item)
    # comments = Comment.objects.filter(item=id).order_by('-date')

    # def _sort_comments(id):
    #     _sort_comments()

    context = {
        'item': item,
        'images': images,
        'attrs': attrs,
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
    all_items = Item.objects.filter(category__in=Category.objects.filter(folder=category))
    all_images = Image.objects.all()

    context = {
        'all_items': all_items,
        'all_images': all_images,
    }

    return render(request, 'market/products.html', context)


def category(request):
    categories = get_list_or_404(Category)

    return render(request, 'market/categories.html', {'categories': categories})


def search(request):
    return render(request, 'market/search.html')
