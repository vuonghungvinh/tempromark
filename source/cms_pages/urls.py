
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    # Index
    url(r'^$',
        views.section_index,
        name='section_page_detail'),

    # Page detail
    url(r'^(?P<slug>[-\w]+)/$',
        views.section_detail,
        name='section_page_detail'),
)
