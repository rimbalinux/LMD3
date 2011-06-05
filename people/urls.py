from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    (r'^$', 'index'),
    (r'^migrate$', 'migrate'),
    #(r'^migrate/delete$', 'migrate_delete'),
    #(r'^repair/livecenter-member-count$', 'repair_livecenter_member_count'),
    #(r'^repair/group-member-count$', 'repair_group_member_count'),
    #(r'^repair/geo-pos$', 'repair_geo_pos'),
    (r'^repair/mobile$', 'repair_mobile'),
    (r'^repair/address$', 'repair_address'),
    (r'^repair/spouse-name$', 'repair_spouse_name'),
    (r'^repair/monthly-income$', 'repair_monthly_income'),
    #(r'^location-not-found$', 'location_not_found'),
    (r'^show/(?P<pid>.*)$', 'show'),
    (r'^create/(?P<lid>.*)$', 'create'),
    (r'^edit/(?P<pid>.*)$', 'edit'),
    (r'^delete/(?P<pid>.*)$', 'delete'),
)
