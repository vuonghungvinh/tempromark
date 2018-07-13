"""
Template tags and filters that are available by default.
"""

from django import template
from django.contrib.humanize.templatetags import humanize
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils import safestring


register = template.Library()


@register.filter
def currency(amount, prefix='$'):
    """
    Format currency value with two decimal points, commas and a symbol prefix.
    The symbol defaults to '$', and can optionally be overridden.

    =============================   ==================
    Usage                           Output
    =============================   ==================
    {{ item.price|currency }}       "$19.95"
    {{ 10.5|currency }}             "$10.50"
    {{ 1000000|currency:"NZD$" }}   "NZD$1,000,000.00"
    {{ 1.9|currency:"" }}           "1.90"
    =============================   ==================

    Using filter on a non-numeric value will result in an empty string.
    """
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return ''
    dollars = humanize.intcomma(int(amount))
    cents = ("%0.2f" % amount)[-3:]
    return "%s%s%s" % (prefix, dollars, cents)


@register.filter
@stringfilter
def email(value, autoescape=None):
    """
    Build 'mailto' link from email address, with a little obsufcation.
    """
    if autoescape:
        value = conditional_escape(value)
    url = entities("mailto:" + value)
    link = '<a href="{0}">{1}</a>'.format(url, entities(value))
    return safestring.mark_safe(link)
email.needs_autoescape = True


@register.filter
@stringfilter
def entities(value, autoescape=None):
    """
    Replace all characters in input string with html hexadecimal entities.
    """
    if autoescape:
        value = conditional_escape(value)
    output = ''.join("&#%s;" % hex(ord(x))[1:] for x in value)
    return safestring.mark_safe(output)
entities.needs_autoescape = True


@register.filter
def pdb(element):
    import pdb; pdb.set_trace()
    return element


@register.filter
@stringfilter
def replace(value, replacement):
    """
    Case-sensitive find-and-replace filter.

    As Django filters can only take one formal argument, the find and
    replace tokens are passed in within a single argument using the
    string " with " as the delimiter.  An example will make this more clear:

    {{ some_var|replace:"needle with haystack"}}
    All occurrences of "needle" in some_var will be replaced with 'haystack'.
    """
    old, new = replacement.split(' with ')
    return value.replace(old, new)
replace.is_safe = True


class SnippetNode(template.Node):
    """
    Node object for snippet tag.
    """
    def __init__(self, nodelist, variable_name):
        self.nodelist = nodelist
        self.variable_name = variable_name

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.variable_name] = output
        return ''


@register.tag
def snippet(parser, token):
    """
    The snippet tag assigns its contents to a template variable.

    It can be used to avoid code duplication when the same content needs to
    be printed more than once, eg. printing escaped and unescaped copies of
    the same JavaScript or HTML code.

    By default snippet contents are put into the context variable 'snippet'::

        {% snippet %}
        ...content...
        {% endsnippet %}

        {{ snippet }}
        {{ snippet }}

    The context variable name can also be over-ridden::

        {% snippet as example01 %}
        ...content...
        {% endsnippet %}

        {{ example01 }}
        {{ example02 }}
    """
    # Get contents
    nodelist = parser.parse(('endsnippet',))
    parser.delete_first_token()

    # Custom variable name?
    args = token.split_contents()
    tag_name = args[0]
    if len(args) == 1:
        variable_name = 'snippet'
    else:
        if len(args) != 3 or args[1] != 'as':
            message = "{0} tag has invalid arguments".format(tag_name)
            raise template.TemplateSyntaxError(message)
        variable_name = args[2]
    return SnippetNode(nodelist, variable_name)
