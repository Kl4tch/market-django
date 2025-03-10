"""kurs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from market import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.category),
    path('index', views.index, name='main2'),
    path('test', views.test, name='test'),
    path('category/<str:category>/', views.products),
    path('<str:slug>/<int:id>/', views.detail),
    # path('<str:slug>/<int:id>/add', views.add),
    # path('<str:slug>/<int:id>/add_review', views.add_review),
    # path('category/<str:category>/search', views.searchAll),
    path('category/<str:category>/search', views.products),
    path('search', views.searchAll),
    path('feedback', views.feedback),
    path('about', views.about),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
