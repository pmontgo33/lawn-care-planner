"""
sitemap.py

This code uses the Django documentation for static views:
https://docs.djangoproject.com/en/1.10/ref/contrib/sitemaps/
"""

# import statements
from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'lawn_new', 'lawn_list', 'feedback']

    def location(self, item):
        return reverse(item)