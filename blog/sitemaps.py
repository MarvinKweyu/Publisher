from django.contrib.sitemaps import Sitemap

from blog.models import Post

"""Generate sitemap: https://docs.djangoproject.com/en/3.0/ref/contrib/sitemaps/#django.contrib.sitemaps.Sitemap.changefreq"""


class PostSitemap(Sitemap):
    changefreq = "hourly"
    # max value is 1
    priority = 0.9

    def items(self):
        """Objects to include in sitemap. Call get_absolute_url by default"""
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
