from django.conf.urls.defaults import *

urlpatterns = patterns('attachment.views',
    (r'^no-container$', 'no_container'),
    (r'^id/(?P<fid>.*)$', 'imgid'),
    (r'^delete/(?P<fid>.*)$', 'delete'),
    (r'^(?P<fid>.*)$', 'image'),
)
