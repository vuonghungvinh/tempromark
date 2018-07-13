"""
Settings that are unique to a production environment.
"""

from .base import *


DEBUG = False


# Caches
#########
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'KEY_PREFIX': CACHE_KEY_PREFIX,
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.PythonParser'
        },
    },
}


#~ DATABASES = {
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #~ 'NAME': 'animal3',
        #~ 'HOST': 'localhost',
        #~ 'OPTIONS': {
            #~ 'autocommit': True,
        #~ },
        #~ 'PASSWORD': 'CYbEXtKsXdspk',
        #~ 'USER': 'animal3',
    #~ },
#~ }


# Email
########
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Sessions
###########
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Static Files
###############
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


# Templates
############
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = ''
TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )


# Applications
###############
from .settings import *
INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTY_APPS + LOCAL_APPS
