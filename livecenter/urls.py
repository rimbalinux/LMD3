from django.conf.urls.defaults import *

urlpatterns = patterns('livecenter.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/$', 'create'),
    (r'^district/(?P<pid>.*)$', 'district'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
    (r'^migrate$', 'migrate'),
    (r'^location/migrate$', 'location_migrate'),
    (r'^category/migrate$', 'category_migrate'),
    (r'^cluster/migrate$', 'cluster_migrate'),
    (r'^category/(?P<pid>.*)$', 'category'),
    (r'^cluster/(?P<pid>.*)$', 'cluster'),
    (r'^nomobile/(?P<pid>.*)$', 'nomobile'),
)
