"""
planner/urls.py
"""

# import statements
from django.conf.urls import url
from django.views.generic import ListView
from planner import views
from planner.models import Lawn
from planner.views import LawnDetailView, ProfileUpdate, UserDetailView, UserLawnListView, LawnDeleteView,\
    LawnNewView, LawnEditView

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    
    url(r'^$', views.index, name="index"),
    url(r'planner/$', LawnNewView.as_view(), name='lawn_new'),
    url(r'^planner/lawn/(?P<pk>\d+)/$', LawnDetailView.as_view(), name="lawn_detail"),
    url(r'^planner/lawn/(?P<pk>\d+)/edit/$', LawnEditView.as_view(), name='lawn_edit'),
    url(r'^planner/lawn/list/$', ListView.as_view(
                        queryset=Lawn.objects.filter(user__username="examples").order_by('name'),
                        template_name="planner/lawn_list.html"), name="example_lawn_list"),
    url(r'^planner/lawn/(?P<pk>\d+)/delete/$', LawnDeleteView.as_view(), name="lawn_delete"),
    url(r'^accounts/profile/$', UserDetailView.as_view(), name="account_profile"),
    url(r'^accounts/profile/edit/$', ProfileUpdate.as_view(), name="account_profile_edit"),
    url(r'^planner/mylawns/$', UserLawnListView.as_view(), name="user_lawn_list"),


    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    ]