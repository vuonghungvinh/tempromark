"""
Settings intended to be modified easily.
"""

# Date Format
##############
# https://docs.djangoproject.com/en/1.5/ref/templates/builtins/#date
DATE_FORMAT = 'N j, Y'
DATE_FORMAT_SHORT = 'Y-m-d'
DATETIME_FORMAT = 'D j M Y H:i T'
DATETIME_FORMAT_SHORT = 'Y-m-d P'


# Applications
###############
THIRD_PARTY_APPS = (
    'easy_thumbnails',
)

LOCAL_APPS = (
    'animal3',
    'catalogue',
    'cms_pages',
    'colours',
    'projects',
    'share_page',
)


# easy-thumbnails
##################
# http://easy-thumbnails.readthedocs.org/
THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_DEBUG = False
THUMBNAIL_EXTENSION = 'jpg'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)
THUMBNAIL_QUALITY = 100
THUMBNAIL_ALIASES = {
    '': {
        'large': {
            'autocrop': False,
            'crop': 'smart',
            'size': (180, 120),
            'upscale': True,
        },
        'small': {
            'autocrop': False,
            'crop': 'smart',
            'size': (165, 105),
            'upscale': True,
        },
        'thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (110, 70),
            'upscale': True,
        },
    },
    'catalogue': {
        'category-carousel': {
            'autocrop': False,
            'crop': 'smart',
            'size': (700, 295),
            'upscale': True,
        },
        'category-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (255, 255),
            'upscale': True,
        },
        'product-gallery': {
            'autocrop': False,
            'crop': 'smart',
            'size': (480, 320),
            'upscale': True,
        },
        'product-gallery-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (90, 60),
            'upscale': True,
        },
        'product-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (220, 166),
            'upscale': True,
        },
        'product-nav-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (138, 103),
            'upscale': True,
        },
        'product-related': {
            'autocrop': False,
            'crop': 'smart',
            'size': (165, 105),
            'upscale': True,
        },
    },
    'cms_pages': {
        'cms_homepage': {
            'autocrop': False,
            'crop': 'smart',
            'size': (0, 435),
            'upscale': True,
        },
    },
    'colours': {
        'colour-square': {
            'autocrop': False,
            'crop': 'smart',
            'size': (160, 160),
            'upscale': True,
        },

    },
    'projects': {
        'project-gallery': {
            'autocrop': False,
            'crop': 'smart',
            'size': (480, 320),
            'upscale': True,
        },
        'project-gallery-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (90, 60),
            'upscale': True,
        },
        'project-thumbnail': {
            'autocrop': False,
            'crop': 'smart',
            'size': (220, 166),
            'upscale': True,
        },
        'project-related': {
            'autocrop': False,
            'crop': 'smart',
            'size': (165, 105),
            'upscale': True,
        },
    },
}


# Template Tags
################
# Make common template tags available everywhere
# (Can only be run *after* cache has been configured)
import django.template
django.template.add_to_builtins('django.contrib.humanize.templatetags.humanize')
django.template.add_to_builtins('django.contrib.webdesign.templatetags.webdesign')
django.template.add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')
django.template.add_to_builtins('animal3.templatetags.animal3_builtins')
