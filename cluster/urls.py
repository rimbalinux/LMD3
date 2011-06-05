from django.conf.urls.defaults import *

urlpatterns = patterns('cluster.views',
    (r'^create/(?P<lid>.*)$', 'create'),
    (r'^edit/(?P<cid>.*)$', 'edit'),
    (r'^delete/(?P<cid>.*)$', 'delete'),
    (r'^migrate$', 'migrate'),
    (r'^migrate/delete$', 'migrate_delete'),
)
