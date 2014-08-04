'''
Created on Aug 3, 2014

@author: simonhome
'''
from django.conf.urls import patterns, include, url
from rango import views

urlpatterns = patterns('',
                       url(r'index',views.index,name='index'),
                       url(r'about',views.about,name='about'))
