"""
A set of request processors that return dictionaries to be merged into a
template context.
"""

from django.conf import settings


def meta(request):
    """
    Adds metadata-related context variables to the context.
    """
    return {
        'META_COPYRIGHT': settings.META_COPYRIGHT,
        'META_DESCRIPTION': settings.META_DESCRIPTION,
        'META_KEYWORDS': settings.META_KEYWORDS,
        'META_NAME': settings.META_NAME,
    }
