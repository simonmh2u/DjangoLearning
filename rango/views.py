from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rango.models import Category, Page

# Create your views here.


def index(request):
    context = RequestContext(request)
    categories = Category.objects.order_by('-likes')[:5]
    con_dict = {'categories': categories}
    pages = Page.objects.order_by('-views')[:5]
    con_dict['pages'] = pages

    for category in categories:
        category.url = category.name.replace(' ', '_')
    return render_to_response('rango/index.html', con_dict, context)


def about(request):
    return render_to_response('rango/about.html')


def category(request, category_name_url):
    context_dict = {}
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict['category_name'] = category_name

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)
