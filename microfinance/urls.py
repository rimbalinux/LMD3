from django.conf.urls.defaults import *

urlpatterns = patterns('microfinance.views',
    (r'^$', 'index'),
    (r'^migrate$', 'migrate'),
    #(r'^migrate/delete$', 'migrate_delete'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/$', 'create'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
)
