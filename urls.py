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
    (r'^dictionary$', 'translate.views.dictionary'),
    (r'^livecenter/', include('livecenter.urls')),
    (r'^cluster/', include('cluster.urls')),
    (r'^people/', include('people.urls')),
    (r'^group/', include('group.urls')),
    (r'^product/', include('product.urls')),
    (r'^microfinance/', include('microfinance.urls')),
    (r'^transaction/', include('transaction.urls')),
    (r'^img/', include('attachment.urls')),
    #(r'^user/migrate', 'user.views.migrate'),
    #(r'^counter/migrate', 'counter.views.migrate'),
    (r'^$', 'home.views.index'),
    (r'^accounts/', include('registration.backends.default.urls')),

)
