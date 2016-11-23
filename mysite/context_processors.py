"""
mysite/context_processors.py
Patrick W. Montgomery
created: 11/22/2016
"""

from django.conf import settings

def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    vars = {}
    if not settings.DEBUG and ga_key:
        vars = {
            'GOOGLE_ANALYTICS_KEY': ga_key,
        }
    return vars