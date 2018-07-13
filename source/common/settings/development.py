"""
Settings that are unique to the development environment.
"""

from .base import *


DEBUG = True


# Authentication
#################
PASSWORD_HASHERS = (
    # Use SHA1 over PBKDF2 to greatly speed-up tests
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)


# Cache
########
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEYPREFIX': SITE_DOMAIN,
    }
}


# Email
########
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Sessions
###########
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


# Static Files
###############
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# Templates
############
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = '<INVALID:%s>'
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)


# Applications
###############
from .settings import *


# Debug Toolbar
# http://pypi.python.org/pypi/django-debug-toolbar
THIRD_PARTY_APPS += ('debug_toolbar',)

INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + LOCAL_APPS
