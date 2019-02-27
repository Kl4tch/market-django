from django.shortcuts import render, redirect
from user.models import User, Cart
from .forms import UserForm, UserAuth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def main(request):

    try:
        token = request.session['access_token']
        profile = User.objects.get(access_token=token)
        items = []

        try:
            items = Cart.objects.filter(user=profile)

        finally:
            context = {
                'user': profile,
                'items': items,
            }

            return render(request, 'market/user/user.html', context)

    except:
        return render(request, 'market/user/user.html')


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарагестрированы!')
            return redirect(main)

    return render(request, 'market/user/register.html', {'form': form})


def logout(request):
    request.session['access_token'] = None
    return redirect(main)


def login(request):
    form1 = UserAuth()
    return render(request, 'market/user/login.html', {'form': form1})
