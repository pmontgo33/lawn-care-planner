"""
contact/forms.py
Patrick W. Montgomery
created: 11-21-2016
"""

from django import forms

class ContactForm(forms.Form):
    
    # Form Fields
    contact_name = forms.CharField(required=True)
    contact_email =  forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "Feedback:"
    