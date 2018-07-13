"""
Template tags for the section application.
"""
import datetime

from django import template

from .. import models

register = template.Library()

@register.inclusion_tag('cms_pages/templatetags/page_navigation.html')
def section_page_navigation(section):
    """
    Renders list of pages for the current section, using template.
    """
    pages = models.Page.objects.filter(section=section)
    return {'pages': pages,}
