from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
)
