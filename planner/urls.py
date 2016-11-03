# planner/urls.py
# Patrick W. Montgomery
# created: 10-8-2016

# import statements
from django.conf.urls import url
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from . import views
from planner.models import Lawn

urlpatterns = [
    
    url(r'^$', views.index, name="index"),
    
    url(r'planner/$', views.lawn_new, name="lawn_new"),
    
    url(r'^planner/lawn/(?P<pk>\d+)/$', views.lawn_detail, name="lawn_detail"),
    
    url(r'^planner/lawn/list/$', ListView.as_view(
                        queryset=Lawn.objects.all(),
                        template_name="planner/lawn_list.html")),
    
#    url(r'planner/lawn/new/$', views.lawn_new, name="lawn_new")
    
    ]
    
    