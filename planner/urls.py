"""
planner/urls.py
"""

# import statements
from django.conf.urls import url
from django.views.generic import ListView
from . import views
from planner.models import Lawn

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    
    url(r'^$', views.index, name="index"),
    url(r'planner/$', views.lawn_new, name="lawn_new"),
    url(r'^planner/lawn/(?P<pk>\d+)/$', views.lawn_detail, name="lawn_detail"),
    url(r'^planner/lawn/list/$', ListView.as_view(
                        queryset=Lawn.objects.filter(user__username="examples").order_by('name'),
                        template_name="planner/lawn_list.html"), name="lawn_list"),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
    ]
    
    