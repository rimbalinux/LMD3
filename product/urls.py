from django.conf.urls.defaults import *

urlpatterns = patterns('product.views',
    (r'^$', 'index'),
    #(r'^migrate$', 'migrate'),
    #(r'^migrate/delete$', 'migrate_delete'),
    #(r'^types$', 'types'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/(?P<pid>.*)$', 'create'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
)
