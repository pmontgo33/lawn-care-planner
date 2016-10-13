# planner/forms.py
# Patrick W. Montgomery
# created: 10/12/2016

from django import forms
from .models import Lawn

class LawnForm(forms.ModelForm):
    
    class Meta:
        model = Lawn
        
        fields = ('zip_code', 'grass_type', 'size')