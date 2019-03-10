from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget


admin.site.register(Brand)
admin.site.register(Discount)
admin.site.register(DiscountItem)


class Imageline(admin.StackedInline):
    model = Image
    extra = 1


class FilterDetailLine(admin.StackedInline):
    model = FilterDetail
    extra = 1


class FilterNameAdmin(admin.ModelAdmin):
    model = FilterName
    inlines = [FilterDetailLine, ]


class ItemDetailLine(admin.StackedInline):
    model = ItemDetail
    extra = 1


class FilterNameLine(admin.StackedInline):
    model = FilterName
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [FilterNameLine, ]


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'is_enabled')
    inlines = [Imageline, ItemDetailLine, ]
    search_fields = ['title', ]
    list_per_page = 20



admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FilterName, FilterNameAdmin)
