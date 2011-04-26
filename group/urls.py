from django.conf.urls.defaults import *

urlpatterns = patterns('group.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
)
