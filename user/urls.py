from django.urls import path
from .viewVK import get_credential, get_token
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('get', get_credential),
    path('token/', get_token),
    path('', main),
    path('login', views.LoginView.as_view(template_name='market/user/login.html')),
    path('logout', logout),
    path('reg', register),
]
