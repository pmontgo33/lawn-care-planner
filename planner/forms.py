# planner/forms.py
# Patrick W. Montgomery
# created: 10/12/2016

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Lawn
from planner.lawn import lawnutils

class LawnForm(forms.ModelForm):
    
    class Meta:
        model = Lawn
        
        fields = ('zip_code', 'grass_type', 'size')
        
        labels = {
            'size': _('Lawn Size (square feet)'),
        }
        
    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        
        if not lawnutils.zip_is_valid(zip_code):
            raise forms.ValidationError("Invalid ZIP code")
        return zip_code
        