from django.shortcuts import render, redirect
from user.models import Profile, Cart


def main(request):

    try:
        token = request.session['access_token']
        profile = Profile.objects.get(access_token=token)
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


def logout(request):
    request.session['access_token'] = None
    return redirect(main)
