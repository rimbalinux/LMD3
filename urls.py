from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}

urlpatterns = patterns('',
    (r'^$', 'msisdn.views.area'),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', 'robots.views.robots'),
    (r'^msisdn/', 'msisdn.views.area'),
    (r'^login/', 'user.views.login'),
    (r'^logout/', 'user.views.logout'),
    (r'^lang/(?P<lang_id>.*)$', 'translate.views.lang'),
)
