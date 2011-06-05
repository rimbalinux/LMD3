from django.conf.urls.defaults import *

urlpatterns = patterns('attachment.views',
    #(r'^migrate$', 'migrate'),
    #(r'^migrate/delete$', 'migrate_delete'),
    #(r'^no-container$', 'no_container'),
    (r'^delete/(?P<fid>.*)$', 'delete'),
    (r'^(?P<fid>.*)$', 'image'),
    (r'^$', 'default'),
)
