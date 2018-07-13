
import django.contrib.sitemaps


class StaticPagesSitemap(django.contrib.sitemaps.Sitemap):
    """
    Sitemap class for static pages.
    """
    pages = {
        '/': (1.0, 'weekly'),
        '/contact/': (0.5, 'yearly'),
    }

    def items(self):
        return self.pages.keys()

    def changefreq(self, url):
        return self.pages[url][1]

    def location(self, url):
        return url

    def priority(self, url):
        return self.pages[url][0]
