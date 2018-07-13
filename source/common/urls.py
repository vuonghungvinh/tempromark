
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as sitemaps_view
from django.views.generic import TemplateView

import catalogue.urls
import catalogue.views
import colours.urls
import cms_pages.urls
import cms_pages.views
import projects.urls
import share_page.urls

from .sitemaps import StaticPagesSitemap


# Static views
urlpatterns = patterns('',
    url(r'^gallery/$',
        TemplateView.as_view(template_name='common/gallery.html')),
)


# Applications
urlpatterns += patterns('',
    (r'^catalogue/', include(catalogue.urls)),
    (r'^color-ranges/', include(colours.urls)),
    (r'^projects/', include(projects.urls)),
    (r'^share/', include(share_page.urls))
)


# CMS Pages
urlpatterns += patterns('',
    url(r'^$',
        cms_pages.views.basic_page, {'slug': 'home'}, name='cms-index'),
    url(r'^contact/$',
        cms_pages.views.basic_page, {'slug': 'contact'}, name='cms-contact'),

    url(r'cms/images/json/(?P<pk>[\d]+)/$',
        cms_pages.views.page_images_json,
        name='cms-images-json'),
    url(r'^about/', include(cms_pages.urls),
        {'section': cms_pages.models.Page.ABOUT}),
    url(r'^support/', include(cms_pages.urls),
        {'section': cms_pages.models.Page.SUPPORT}),
    url(r'^admin/cms-page/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$',
        cms_pages.views.admin_move_ordered_model, name="admin-cms-move"),
    url(r'^admin/catalogue/category/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$',
        catalogue.views.admin_move_ordered_model, name="admin-category-move"),
    url(r'^admin/catalogue/files/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$',
        catalogue.views.admin_move_ordered_model, name="admin-files-move"),
)


# Sitemaps
sitemaps = {
    'static': StaticPagesSitemap,
}
urlpatterns += patterns('',
    (r'^sitemap\.xml$', sitemaps_view, {'sitemaps': sitemaps}),
)


# Admin Interface
admin.autodiscover()
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)


# Debug serving of media files
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
