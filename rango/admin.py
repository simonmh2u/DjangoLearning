from django.contrib import admin
from rango.models import Category, Page

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    fields = ['category','title', 'url', 'views']
    list_display = ('title', 'category', 'url')
    list_filter = ['category']

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
