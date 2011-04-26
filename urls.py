from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', 'robots.views.robots'),
    (r'^login/', 'user.views.login'),
    (r'^logout/', 'user.views.logout'),
    (r'^lang/(?P<lang_id>.*)$', 'translate.views.lang'),
    (r'^migrasi/user', 'migrasi.views.user'),
    (r'^livecenter/$', 'livecenter.views.index'),
    (r'^livecenter/show/(?P<pid>.*)$', 'livecenter.views.show'),
    (r'^livecenter/create/$', 'livecenter.views.create'),
    (r'^livecenter/district/(?P<pid>.*)$', 'livecenter.views.district'),
    (r'^livecenter/edit/(?P<pid>.*)$', 'livecenter.views.edit'),
    (r'^livecenter/delete/(?P<pid>.*)$', 'livecenter.views.delete'),
    (r'^people/$', 'people.views.index'),
    (r'^people/show/(?P<pid>.*)$', 'people.views.show'),
    (r'^group/$', 'group.views.index'),
    (r'^group/show/(?P<pid>.*)$', 'group.views.show'),
    (r'^product/$', 'product.views.index'),
    (r'^product/show/(?P<pid>.*)$', 'product.views.show'),
    (r'^microfinance/$', 'microfinance.views.index'),
    (r'^microfinance/show/(?P<pid>.*)$', 'microfinance.views.show'),
    (r'^microfinance/create/$', 'microfinance.views.create'),
    (r'^microfinance/delete/(?P<pid>.*)$', 'microfinance.views.delete'),
    (r'^microfinance/edit/(?P<pid>.*)$', 'microfinance.views.edit'),
    (r'^img/(?P<file_id>.*)$', 'attachment.views.image'),
    (r'^$', 'home.views.index'),
)
