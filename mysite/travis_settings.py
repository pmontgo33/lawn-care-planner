from .settings import *

SECRET_KEY = "SecretKeyForUseOnTravis"
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'test_db',
    'USER': 'postgres',
    }
}
