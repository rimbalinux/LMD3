from livecenter.models import LiveGroup, LiveCenter, MetaForm, Report_Group, \
        GroupTraining
from livecenter.views import DEFAULT_LOCATION
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, group, next = SearchablePagerQuery(LiveGroup).search(q).fetch(8, page)
    return direct_to_template(request, 'group/index.html', {
        'groups': group,
        'groups_count': counter.get('site_group_count'),
        'prev': prev,
        'next': next,
        'lokasi': ', '.join(map(lambda x: str(x), DEFAULT_LOCATION)),
        })

def show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/group')
    category = item.livecluster.category
    return direct_to_template(request, 'group/show.html', {
        'group': item,
        'member_count': item.members.count(),
        'livecenter': LiveCenter.all().filter('__key__', item.livecluster.livecenter[0]).get(),
        'other_groups': LiveGroup.all().filter('livecluster', item.livecluster ).filter('__key__ !=', item.key()),
        'customfields': MetaForm.all().order('__key__').filter('container', category.key()).filter('meta_type', 'group'),
        'report': Report_Group.all().filter('livecluster', item.livecluster ).filter('name_group', item.key()),
        'training': GroupTraining.all().filter('group', item.key()),
        'lokasi': str(item.geo_pos).strip('nan,nan') or ', '.join(DEFAULT_LOCATION),
        })
