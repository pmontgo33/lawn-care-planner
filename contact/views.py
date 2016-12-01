"""
contact/views.py
Patrick W. Montgomery
created: 11/21/2016
"""

# import statements
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

from contact.forms import ContactForm

def feedback(request):
    form_class = ContactForm
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            subject = request.POST.get('subject', '')
            form_content = request.POST.get('content', '')
            
            # Email the profile with the contact information
            template = get_template('contact/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'subject': subject,
                'form_content': form_content,
            })
            content = template.render(context)
            
            email = EmailMessage(
                "LCP: New contact form submission: %s" % (subject),
                content,
                'noreply@lawncareplanner.com',
                ['monty@lawncareplanner.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            return redirect('feedback_thank')
    
    return render(request, 'contact/feedback.html', {'form': form_class})
