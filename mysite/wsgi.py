"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

# The following code was added from the below site in order to setup Heroku
# https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/heroku/

from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)