from django.conf.urls.defaults import *

urlpatterns = patterns('group.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/(?P<lid>.*)/(?P<cid>.*)$', 'create'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
)
