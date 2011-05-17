from django.conf.urls.defaults import *

urlpatterns = patterns('cluster.views',
    (r'^migrate$', 'migrate'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
)
