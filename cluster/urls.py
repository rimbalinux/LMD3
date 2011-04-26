from django.conf.urls.defaults import *

urlpatterns = patterns('cluster.views',
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
)
