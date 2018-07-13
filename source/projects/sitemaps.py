
from django.contrib.sitemaps import Sitemap

from . import models


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.Entry.objects.all()

    def lastmod(self, obj):
        return obj.published
