from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.


def index(request):
    request.session.set_test_cookie()
    context = RequestContext(request)
    categories = Category.objects.order_by('-likes')[:5]
    con_dict = {'categories': categories}
    pages = Page.objects.order_by('-views')[:5]
    con_dict['pages'] = pages
        #### NEW CODE ####
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        
        visits = request.session.get('visits', 0)
        request.session['visits'] = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    #### END NEW CODE ####
    
    for category in categories:
        category.url = category.name.replace(' ','_')
    return render_to_response('rango/index.html', con_dict, context)


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    return render_to_response('rango/about.html',{'count':count})


def category(request, category_name_url):
    context_dict={}
    context = RequestContext(request)
    category_name = category_name_url.replace('_',' ')
    context_dict['category_name'] = category_name
    
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
            
    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html',context_dict,context)
    
@login_required
def add_category(request):
    context = RequestContext(request)
                             
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            form.errors
    else:
        form = CategoryForm()
        
    return render_to_response('rango/category_new.html',{'form':form},context)
        
@login_required        
def add_page(request,category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_',' ')
    if request.method == 'POST':
        form = PageForm(request.POST)
        cat = Category.objects.get(name = category_name)
        if form.is_valid():
            page  = form.save(commit=False)
            page.category = cat
            form.save(commit=True)
            return category(request,category_name_url)
        else:
            form.errors
        
    else:
        form = PageForm()
        
    return render_to_response('rango/page_new.html',{'form':form,'category_name':category_name,'category_name_url':category_name_url},context)


def register(request):
    context = RequestContext(request)
    registered = False
    if request.session.test_cookie_worked():
        print ">>>>>TEST COOKIE WORKED"
        request.session.delete_test_cookie()
    
    if request.POST:
        form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
        
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.picture = request.FILES['picture']            
            profile.save()
            registered = True
        else:
            form.errors, profile_form.errors
        
    else:
        form = UserForm()
        profile_form = UserProfileForm()
    
    return render_to_response('rango/register.html',{'form':form,'profile_form':profile_form,'registered':registered},context)


def user_login(request):
    context = RequestContext(request)
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")        
    else:
        return render_to_response('rango/login.html', {}, context)



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')