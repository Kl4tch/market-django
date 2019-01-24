from django.shortcuts import render
from user.models import Profile


def main(request):

    try:
        token = request.session['access_token']
        profile = Profile.objects.get(access_token=token)

        context = {
            'user': profile,
        }

        return render(request, 'market/user/user.html', context)

    except ():
        return render(request, 'market/user/user.html')
