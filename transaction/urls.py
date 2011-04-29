from django.conf.urls.defaults import *

urlpatterns = patterns('transaction.views',
    (r'^create/(?P<pid>.*)$', 'create'),
    (r'^edit/(?P<tid>.*)$', 'edit'),
)
