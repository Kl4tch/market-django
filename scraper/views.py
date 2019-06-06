from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.management import call_command


def start(request):
    call_command('scraper', interactive=True)


def scraper(request):
    return render(request, 'market/scraper.html')
