import datetime

from django.conf.urls import include, url
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from models import Post

from . import views


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    lastmod = datetime.datetime.now()
    def items(self):
        return Post.objects.all()

sitemaps =  {
    "posts": PostSitemap,
}

urlpatterns = [
    url(r'^index', views.display_post_index),
    url(r'^$', views.display_post),
    url(r'^upload', views.display_upload_page),
    url(r'^search', views.search_post),
    url(r'^handle_upload', views.upload_post),
    url(r'^handle_update', views.update_post),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
