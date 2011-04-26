from django.conf.urls.defaults import *

urlpatterns = patterns('product.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
)
