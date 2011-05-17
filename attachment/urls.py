from django.conf.urls.defaults import *

urlpatterns = patterns('attachment.views',
    (r'^migrate$', 'migrate'),
    (r'^no-container$', 'no_container'),
    (r'^fid/(?P<fid>.*)$', 'imgfid'),
    (r'^id/(?P<fid>.*)$', 'imgid'),
    (r'^delete/(?P<fid>.*)$', 'delete'),
    (r'^(?P<fid>.*)$', 'image'),
)
