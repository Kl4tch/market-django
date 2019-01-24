import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from .models import *


def get_credential(request):
    client_id = settings.VK_CLIENT_ID
    redirect_url = 'http://127.0.0.1:8000/user/token/'
    vk_url = f"https://oauth.vk.com/authorize?client_id={client_id}&display=page&scope=offline&redirect_uri={redirect_url}"
    return HttpResponseRedirect(vk_url)


# api/token/ Получение access_token
def get_token(request):
    created = 0
    if request.method == 'GET':
        redirect_url = 'http://127.0.0.1:8000/user/token/'
        code = request.GET.get("code")
        error = request.GET.get("error")
        auth_url = f'https://oauth.vk.com/access_token?client_id={settings.VK_CLIENT_ID}&client_secret={settings.VK_CLIENT_SECRET}&redirect_uri={redirect_url}&code={code}'
        auth_response = requests.get(
            url=auth_url).json()  # тут идет запрос к вк, метод json преобразовывает ответ в json
        # print(auth_response.text)
        if error or 'error' in auth_response:
            return JsonResponse({"status": "error"})

        access_token = auth_response['access_token']
        user_info = requests.get(f'https://api.vk.com/method/users.get?access_token={access_token}&v=5.92').json()

        first_name = user_info['response'][0]['first_name']
        last_name = user_info['response'][0]['last_name']

        profile, created = Profile.objects.get_or_create(
            vk_id=auth_response["user_id"],
            defaults=dict(
                first_name=first_name,
                last_name=last_name,
                access_token=access_token,
            )
        )

        profile = Profile.objects.get(access_token=profile.access_token)
        request.session['access_token'] = profile.access_token

        context = {
            'user': profile,
        }

        return render(request, 'market/user/user.html', context)
