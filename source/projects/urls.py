
from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from . import views


urlpatterns = patterns('',
    # Index
    url(r'^$',
        views.index,
        name='project_index'),

    # Category detail
    url(r'^entry/(?P<slug>[\w\-]+)/(?P<pk>[\d]+)/$',
        views.category_detail,
        name='project_category_detail'),

    # Entry detail
    url(r'^entry/(?P<slug>[\w\-]+)/$',
        views.entry_detail,
        name='project_entry_detail'),

    # Basic Search
    url(r'^search/$',
        views.search,
        name='project_search'),

    # Redactor JSON
    url(r'json/images/(?P<pk>[\d]+)/$',
        views.entry_images_json,
        name='project_images_json'),
)
