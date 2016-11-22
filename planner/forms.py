# planner/forms.py
# Patrick W. Montgomery
# created: 10/12/2016

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Lawn

class LawnForm(forms.ModelForm):
    
    class Meta:
        model = Lawn
        
        fields = ('zip_code', 'grass_type', 'size')
        
        labels = {
            'size': _('Lawn Size (square feet)'),
        }