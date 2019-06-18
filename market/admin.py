from django.contrib import admin
from .models import *
from scraper.models import StoreItem


admin.site.register(Brand)
admin.site.register(Category)


class ImageLine(admin.StackedInline):
    model = Image
    extra = 1


class ItemDetailLine(admin.StackedInline):
    model = ItemDetail
    extra = 1


class StoreItemLine(admin.StackedInline):
    model = StoreItem
    extra = 1

#
# class FilterNameAdmin(admin.ModelAdmin):
#     model = FilterName
#     inlines = [FilterDetailLine, ]
#
#
# class ItemDetailLine(admin.StackedInline):
#     model = ItemDetail
#     extra = 1
#
#
# class FilterNameLine(admin.StackedInline):
#     model = FilterName
#     extra = 1
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     model = Category
#     inlines = [FilterNameLine, ]


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'is_enabled')
    inlines = [ImageLine, StoreItemLine, ItemDetailLine]
    search_fields = ['title', ]
    list_per_page = 20
    list_filter = ('category', 'brand')


class ItemDetailAdmin(admin.ModelAdmin):
    list_filter = ('item',)

class FeedBackAdmin(admin.ModelAdmin):
    search_fields = ['title', 'phone']
    list_display = ('title', 'answered', )



admin.site.register(FeedBack, FeedBackAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemDetail, ItemDetailAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(FilterName, FilterNameAdmin)
