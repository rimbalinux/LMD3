from django.conf.urls.defaults import *

urlpatterns = patterns('livecenter.views',
    (r'^$', 'index'),
    (r'^migrate$', 'migrate'),
    #(r'^migrate/delete$', 'migrate_delete'),
    (r'^location/migrate$', 'location_migrate'),
    #(r'^location/migrate/delete$', 'location_migrate_delete'),
    (r'^category/migrate$', 'category_migrate'),
    #(r'^category/migrate/delete$', 'category_migrate_delete'),
    (r'^migrate/metaform$', 'migrate_metaform'),
    #(r'^migrate/metaform/delete$', 'migrate_metaform_delete'),
    (r'^show/(?P<lid>.*)$', 'show'),
    (r'^create$', 'create'),
    (r'^district/(?P<pid>.*)$', 'district'),
    (r'^edit/(?P<lid>.*)$', 'edit'),
    (r'^delete/(?P<lid>.*)$', 'delete'),
)
