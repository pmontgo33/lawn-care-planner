"""
This file contains all forms for the planner app
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, Fieldset, Field
from crispy_forms.bootstrap import Tab, TabHolder

from .models import Lawn
from planner.lawn import lawnutils

import logging
logger = logging.getLogger(__name__)

class LawnForm(forms.ModelForm):

    ORGANIC_CHOICES = (
        ('NP', 'No Preference'),
        ('M', 'Mostly Organic'),
        ('A', 'All Organic'),
    )

    ADVANCED_CHOICES = (
        (False, 'Basic'),
        (True, 'Advanced'),
    )

    organic = forms.ChoiceField(choices=ORGANIC_CHOICES, widget=forms.RadioSelect(), initial='NP', label=' ')
    advanced = forms.ChoiceField(choices=ADVANCED_CHOICES, widget=forms.RadioSelect(), initial=False, label='Planner Type')
    class Meta:
        model = Lawn
        fields = ['advanced', 'name', 'zip_code', 'grass_type', 'size', 'weekly_notify', 'phosphorus', 'spring_seeding', 'organic']

        labels = {
            'size': _('Lawn Size (square feet)'),
            'weekly_notify': _('Send me email notifications for upcoming lawn care activites'),
        }

    def __init__(self, user, *args, **kwargs):
        super(LawnForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab('Lawn Details',
                    Div('advanced', type='input', css_id='advanced_input'),
                    Fieldset('General',
                             'name',
                             'zip_code',
                             'grass_type',
                             'size',
                             'weekly_notify',
                    ),
                    Fieldset('Advanceddd',
                             'phosphorus',
                             css_id='advanced_fieldset',
                             style='display:none;'
                    ),
                ),
                Tab('Options',
                    Div(HTML('<p class="col-lg-8"><strong>Spring Seeding: </strong>Seeding in the spring is typically '
                             'not recommended due to increased competition with weeds. LCP recommends seeding only in '
                             'the fall, but there may be circumstances where you want to seed in the spring. '
                             'If so, check below to include it in your planner. </p>'), css_class='row'),
                    'spring_seeding',
                    Div(HTML('<p class="col-lg-8"><strong>Organic: </strong> Mostly organic will recommend good '
                             'organic fertilizers and some chemical weed control. All organic will not provide any '
                             'recommendations with chemicals.</p>'), css_class='row'),
                    'organic',
                ),
                Tab('Advanced',
                ),
            ),
        )

        # self.helper['Lawn Details'].layout.append((HTML('<h1>HERE</h1>')))
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