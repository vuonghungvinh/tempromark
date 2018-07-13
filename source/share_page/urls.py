
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from . import views


urlpatterns = patterns(
    '',

    url(r'^$',
        views.process_form,
        name='share'),

    url(r'^thanks/$',
        TemplateView.as_view(template_name='share_page/thanks.html'),
        name='share-thanks'),
)
