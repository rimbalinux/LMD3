from django.conf.urls.defaults import *

urlpatterns = patterns('group.views',
    (r'^$', 'index'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/(?P<lid>.*)/(?P<cid>.*)$', 'create'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^add_report/(?P<pid>.*)$', 'add_report'),
    (r'^report_show/(?P<pid>.*)$', 'report_show'),
    (r'^report_delete/(?P<pid>.*)$', 'report_delete'),
    (r'^edit_report/(?P<pid>.*)$', 'edit_report'),
    (r'^add_training/(?P<pid>.*)$', 'add_training'),
    (r'^edit_training/(?P<pid>.*)$', 'edit_training'),
    (r'^map/(?P<pid>.*)$', 'map'),
)
