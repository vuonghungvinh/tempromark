
import re

from django.http import Http404
from django.template import TemplateDoesNotExist
from django.shortcuts import render


def static(request, name, folder):
    template = name[:-1] if name else 'index'
    try:
        template = re.sub('[^\w\-]', '', template)      # Avoid path traversal
        template = "{1}/{0}.html".format(template, folder)
        return render(request, template)
    except TemplateDoesNotExist:
        raise Http404('Template not found: {}'.format(template))
