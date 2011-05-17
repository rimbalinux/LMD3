from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    (r'^$', 'index'),
    (r'^migrate$', 'migrate'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/(?P<lid>.*)$', 'create'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
    (r'^group/(?P<pid>.*)$', 'group'),
)
