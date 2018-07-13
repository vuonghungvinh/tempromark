"""
Template tags for the share page application.
"""

from django import template

from share_page import forms


register = template.Library()


@register.inclusion_tag('share_page/form.html')
def share_form(request):
    if request.method == 'POST':
        form = forms.ShareForm(request.POST, path=request.path)
    else:
        form = forms.ShareForm(path=request.path)
    return {'form': form}
