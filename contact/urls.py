"""
contact/urls.py
Patrick W. Montgomery
created: 11-21-2016
"""

# import statements
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    
    url(r'^feedback/$', views.feedback, name="feedback"),
    url(r'^feedback/thankyou/$', TemplateView.as_view(template_name="contact/feedback_thank.html"), name="feedback_thank"),
    
    ]
    
    