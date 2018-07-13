"""
Template tags for the blog application.
"""

from django import template

from .. import models


register = template.Library()


@register.inclusion_tag('projects/templatetags/entry-featured.html')
def blog_entry_featured(entry):
    """
    Render summary template for given featured entry, using template.

    Requires an entry object as a parameter.

    Usage::
        {% for entry in entries %}
            {% blog_entry_featured entry %}
        {% endfor %}
    """
    return {'entry': entry}


@register.inclusion_tag('projects/templatetags/entry-summary.html')
def blog_entry_summary(entry):
    """
    Render summary template for given entry, using template.

    Requires an entry object as a parameter.

    Usage::
        {% for entry in entries %}
            {% blog_entry_summary entry %}
        {% endfor %}
    """
    return {'entry': entry}


@register.inclusion_tag('projects/templatetags/entries-latest.html')
def blog_latest_entries(limit=None):
    """
    Renders a list of the most recent blog entries.

    Usage::
        <ul>
            {% blog_latest_entries limit=5 %}
        </ul>
    """
    entries = models.Entry.objects.get_published()[:limit]
    return {'entries': entries}


@register.inclusion_tag('projects/templatetags/entries-featured.html')
def blog_featured_entries(limit=None):
    """
    Renders a list of featured blog entries.

    Usage::
        <ul>
            {% blog_get_featured_entries limt=5 %}
        </ul>
    """
    entries = models.Entry.objects.get_published().order_by('?').filter(featured=True)[:limit]
    return {'entries': entries}


@register.inclusion_tag('projects/templatetags/navigation.html')
def blog_navigation():
    categories = models.Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('projects/templatetags/related-entries.html')
def related_entries(entry, limit=2):
    category = entry.category
    entries = entries = category.entries.exclude(pk=entry.pk)[:limit]
    return {'entries': entries}

