from livecenter.models import LiveGroup, LiveCenter, MetaForm, Report_Group, \
        GroupTraining, LiveCluster
from livecenter.views import default_location
from livecenter.utils import redirect
from attachment.utils import save_file_upload
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, group, next = SearchablePagerQuery(LiveGroup).\
            search(q).fetch(8, page)
    return direct_to_template(request, 'group/index.html', {
        'groups': group,
        'groups_count': counter.get('site_group_count'),
        'prev': prev,
        'next': next,
        'lokasi': default_location(), 
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
        'lokasi': str(item.geo_pos).strip('nan,nan') or default_location(),
        })

def create(request, lid, cid):
    lc = db.get(db.Key(lid))
    cluster = db.get(db.Key(cid))
    customfields = MetaForm.all().order('__key__').\
            filter('meta_type', 'group').\
            filter('container', cluster.category.key())
    if request.POST:
        save(request, lc, cluster, customfields)
        return redirect(request, '/group')
    category = cluster.category
    return direct_to_template(request, 'group/create.html', {
        'livecenter': lc,
        'cluster': cluster,
        'clusters': LiveCluster.all().filter('livecenter', lc.key()).\
                filter('category', category.key()),
        'customfields': customfields,
        })

def save(request, lc, cluster, customfields): 
    item = LiveGroup()
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.livecluster = cluster.key()
    item.containers.append(lc.key())
    if request.POST['geo_pos']:
        item.geo_pos = request.POST['geo_pos']
    item.put()
    save_file_upload(request, 'photo', item)
    for meta in customfields:
        if request.POST[meta.slug]:
            try:
                if meta.form_type == 'file':
                    if not request.POST[meta.slug]:
                        continue
                    val = db.Blob(request.POST[meta.slug])
                    setattr(item, meta.slug, val)
                else:
                    setattr(item, meta.slug, request.POST[meta.slug])
            except:
                pass
    item.put()
    return item

def delete(request, pid):
    item = db.get(pid)
    if item:
        item.delete()
        counter.update('site_group_count', -1)
    return redirect(request, '/group')
