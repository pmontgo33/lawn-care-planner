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
    
    # Planner index page - NEED TO ADD FILTER BY USER
    url(r'^$', ListView.as_view(
                        queryset=Lawn.objects.all(),
                        template_name="planner/lawn_list.html")),
    
    url(r'^lawn/(?P<pk>\d+)/$', views.lawn_detail, name="lawn_detail"),
    
    url(r'lawn/new/$', views.lawn_new, name="lawn_new")
    
    ]
    
    