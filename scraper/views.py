from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.management import call_command
from scraper.forms import Form


def scraper(request):
    context = {
        'form': Form,
    }
    return render(request, 'market/scraper.html', context)


def start(request):
    url = request.GET.get('url')
    category = request.GET.get('category')
    startPage = request.GET.get('startPage')
    endPage = request.GET.get('endPage')

    # call_command('scraper', url=url, category=category, startPage=startPage, endPage=endPage)
    call_command('scraper', url, category, startPage, endPage)

    return redirect('/')
