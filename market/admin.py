from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(FilterName)
admin.site.register(ItemDetail)
admin.site.register(FilterDetail)
admin.site.register(Brand)