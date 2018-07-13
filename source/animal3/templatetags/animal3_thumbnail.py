"""
Custom `thumbnail` tag to replace the one from `django-easy-thumbnails`.

Requires that `django-easy-thumbnails` be installed and configured properly.
"""

from django import template
from django.core.exceptions import ImproperlyConfigured

import easy_thumbnails.files


register = template.Library()


@register.simple_tag
def thumbnail(image, alias, **extras):
    """
    Output HTML IMG tag using the excellent `django-easy-thumbnails` package.

    image
        A model file or image field.
    alias
        A string reference to a dictionary in settings.THUMBNAIL_ALIASES
    extras
        Extra HTML attributes to add to IMG tag.
    """
    thumb = _create_thumb(image, alias)
    attributes = {}
    attributes['src'] = thumb.url
    attributes['width'] = thumb.width
    attributes['height'] = thumb.height
    attributes.update(extras)
    if 'alt' not in attributes:
        attributes['alt'] = ''
    return "<img {} />".format(' '.join('{}="{}"'.format(
        key, attributes[key]) for key in sorted(attributes)))


@register.simple_tag
def thumbnail_url(image, alias, **extras):
    """
    Like `thumbnail`, but produces just a bare URL to the thumbnail image.

    Width and height information is discarded.
    """
    thumb = _create_thumb(image, alias)
    return thumb.url


def _create_thumb(image, alias):
    """
    Create easy-thumbnail thumbnail using parameters from given alias
    """
    # Create name to match against alias (eg. 'users.Profile.cover_image')
    field_name = image.field.name
    model_name = image.instance.__class__.__name__
    app_name = image.instance.__class__.__module__.split('.')[0]
    target = "{}.{}.{}".format(app_name, model_name, field_name)

    # Match alias and create thumbnail
    thumbnailer = easy_thumbnails.files.get_thumbnailer(image)
    thumbnail_options = easy_thumbnails.alias.aliases.get(alias, target)
    if not thumbnail_options:
        raise ImproperlyConfigured(
            "Thumbnail alias not found for: {}['{}']".format(target, alias))
    return thumbnailer.get_thumbnail(thumbnail_options)
