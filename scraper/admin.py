from django.contrib import admin
from .models import *


class AttributeTitleAdmin(admin.ModelAdmin):
    list_filter = ('bigTitle', )


class AttributeValueAdmin(admin.ModelAdmin):
    list_filter = ('attributeTitle', )


class StoreItemAdmin(admin.ModelAdmin):
    list_filter = ('store', 'item',)


admin.site.register(Store)
admin.site.register(StoreItem, StoreItemAdmin)
admin.site.register(GroupTitle)
admin.site.register(AttributeTitle, AttributeTitleAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
