SECRET_KEY = "SecretKeyForUseOnTravis"
from .settings import *
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'test_db',
    'USER': 'postgres',
    }
}
