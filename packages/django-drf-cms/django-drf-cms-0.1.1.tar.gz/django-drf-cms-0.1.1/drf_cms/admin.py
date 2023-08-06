from django.contrib import admin
from .models import *

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    model = Page
    list_filter = ('site',)

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    model = Text
    list_display = ('key', 'page', )
    list_filter = ('page', 'page__site')
