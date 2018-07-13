"""
Base machinery for settings.
"""


import os.path

from django.utils import six


# Paths
########
SITE_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SITE_DOMAIN = os.path.basename(SITE_ROOT)

DATA_ROOT = os.path.join(SITE_ROOT, 'data')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
SOURCE_ROOT = os.path.join(SITE_ROOT, 'source')
STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(SITE_ROOT, 's')
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SETTINGS_INI = os.path.join(SITE_ROOT, 'settings.ini')
TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'),)
TEST_ROOT = os.path.join(SITE_ROOT, 'tests')


# settings.ini
###############
if six.PY3:
    from configparser import ConfigParser
else:
    from ConfigParser import SafeConfigParser as ConfigParser

settings_ini = ConfigParser()
settings_ini.read(SETTINGS_INI)

def clean_multiline(text):
    "Convert multiline setting value into a long single-line string"
    text = text.replace('\n', ' ')
    return text.strip()

def clean_email(text):
    "Extract email into tuple format, as expected by Django"
    parts = text.split('<')
    name = parts[0].strip()
    email = parts[1][:-1]
    return ((name, email),)


# Applications
###############
BUILT_IN_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
)


# Cache Prefix
###############
CACHE_KEY_PREFIX = SITE_DOMAIN
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_KEY_PREFIX


# Databases
############
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_ROOT, 'db.sqlite3'),
    },
}


# Email
########
META_NAME = settings_ini.get('metadata', 'name')
EMAIL_SUBJECT_PREFIX = '[{0}]'.format(META_NAME)
ADMINS = clean_email(settings_ini.get('email', 'webmaster'))
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = settings_ini.get('email', 'default_from')
SEND_BROKEN_LINK_EMAILS = True


# Messages
##########
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Metadata
###########
META_COPYRIGHT = clean_multiline(settings_ini.get('metadata', 'copyright'))
META_DESCRIPTION = clean_multiline(settings_ini.get('metadata', 'description'))
META_KEYWORDS = clean_multiline(settings_ini.get('metadata', 'keywords'))


# Middleware
#############
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)


# Miscellaneous
################
ALLOWED_HOSTS = ['localhost', '.{}'.format(SITE_DOMAIN)]
APPEND_SLASH = True
FILE_UPLOAD_PERMISSIONS = 420 # 0644 in octal
LANGUAGE_CODE = 'en-NZ'
ROOT_URLCONF = 'common.urls'
SECRET_KEY = '230*hk8xrtkb!4nhr&6d5v0b-dljoga(ddht))4k9gp#!5#m=-'
SITE_ID = 1
USE_I18N = False
USE_L10N = False


# Sessions
###########
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 'session'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 691200     # Eight days


# Templates
###########
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'animal3.context_processors.meta',
)


# Tests
########
# (Run tests only for locally installed apps., not third-party ones)
TEST_RUNNER = 'animal3.utils.LocalTestRunner'


# Time/date
############
USE_TZ = True
TIME_ZONE = 'Pacific/Auckland'
