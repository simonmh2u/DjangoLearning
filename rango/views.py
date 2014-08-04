from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from rango.models import Category

# Create your views here.


def index(request):
    context = RequestContext(request)
    categories = Category.objects.order_by('-likes')[:5]
    con_dict = {'categories': categories}
    return render_to_response('rango/index.html', con_dict, context)


def about(request):
    return render_to_response('rango/about.html')
