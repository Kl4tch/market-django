from django.contrib import admin
from .models import *


class AttributeValueLine(admin.StackedInline):
    model = AttributeValue
    extra = 1


class AttributeTitleLine(admin.StackedInline):
    model = AttributeTitle
    extra = 1


class AttributeTitleAdmin(admin.ModelAdmin):
    list_filter = ('bigTitle', )
    search_fields = ['attr', ]
    list_display = ('attr', 'isFiltered')
    inlines = [AttributeValueLine, ]


class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ['value', ]
    list_filter = ('attributeTitle', )


class GroupTitleAdmin(admin.ModelAdmin):
    search_fields = ['title', ]
    inlines = [AttributeTitleLine, ]


class StoreItemAdmin(admin.ModelAdmin):
    list_filter = ('store', 'item',)
    search_fields = ['item__title', ]


admin.site.register(Store)
admin.site.register(StoreItem, StoreItemAdmin)
admin.site.register(GroupTitle, GroupTitleAdmin)
admin.site.register(AttributeTitle, AttributeTitleAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
