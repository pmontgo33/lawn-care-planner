"""
This file contains all forms for the planner app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Lawn
from planner.lawn import lawnutils


class LawnForm(forms.ModelForm):
    
    class Meta:
        model = Lawn
        fields = ['name', 'zip_code', 'grass_type', 'size', 'weekly_notify']

        labels = {
            'size': _('Lawn Size (square feet)'),
            'weekly_notify': _('Send me email notifications for upcoming lawn care activites'),
        }

    def __init__(self, user, *args, **kwargs):
        super(LawnForm, self).__init__(*args, **kwargs)
        if user.is_anonymous():
            del self.fields['name']
            del self.fields['weekly_notify']

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        
        if not lawnutils.zip_is_valid(zip_code):
            raise forms.ValidationError("Invalid ZIP code")
        return zip_code


class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=45, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=45, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()