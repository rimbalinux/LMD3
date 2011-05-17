from .models import LiveCenter, MicroFinance, Person, LivelihoodLocation, \
        Attachment, LiveCluster, LiveCategory, MetaForm, \
        CategoryContainer, Category, Livelihood, Container, Location
from attachment.models import Attachment, Container as FileContainer
from attachment.utils import save_file_upload
from .utils import getLocation, default_location
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter
import json
import urllib


def index(request):
    items = LiveCenter.all().order('name')
    return direct_to_template(request, 'livecenter/index.html', {
        'livecenters': items,
        'lokasi': default_location(), 
        })

def destination(pid, tabname):
    return urllib.quote('/livecenter/show/%s?tab=%s' % (pid, tabname))

def show(request, pid):
    lc = db.get(pid)
    if not lc:
        return HttpResponseRedirect('/livecenter')
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, members, next = SearchablePagerQuery(Person).filter('livecenter = ', lc.key()).order('-last_modified').fetch(15, page)
    return direct_to_template(request, 'livecenter/show.html', {
        'members': members,
        'members_count': counter.get('lc_member_count_%s' % lc.key().id()),
        'livecenter': lc,
        'prev': prev,
        'next': next,
        'microfinance': MicroFinance.all().filter('district', lc.district.key()).fetch(10),
        'related_livecenter': LiveCenter.all().filter('category IN', lc.category ).filter('__key__ !=', lc.key()).fetch(5),
        'lokasi': str(lc.geo_pos).strip('nan,nan') or default_location(),
        'tab_member': destination(pid, 'member'),
        'tab_cluster': destination(pid, 'cluster'),
        'tab_group': destination(pid, 'group'),
        })

def create(request):
    if request.POST: 
        lc = save(request)
        return HttpResponseRedirect('/livecenter/show/%s' % lc.key())
    return direct_to_template(request, 'livecenter/create.html', {
        'pagetitle': 'Tambah Mata Pencaharian',
        'district_sel': 0,
        'subdistrict_sel': 0,
        'village_sel': 0,
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        })

def edit(request, pid):
    if request.POST:
        lc = save(request, pid)
        if lc:
            return HttpResponseRedirect('/livecenter/show/%s' % lc.key())
        return HttpResponseRedirect('/livecenter')
    lc = db.get(pid)
    return direct_to_template(request, 'livecenter/create.html', {
        'pagetitle': 'Ubah ' + lc.name,
        'livecenter': lc,
        'geo_pos': lc.geo_pos,
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        'district_sel': lc.district.dl_id,
        'subdistrict_sel': lc.sub_district.dl_id,
        'village_sel': lc.village.dl_id,
        })

def save(request, pid=None):
    if pid:
        lc = db.get(pid)
        if not lc:
            return
    else:
        lc = LiveCenter()
    lc.name = request.POST['name']
    lc.address = request.POST['address']
    lc.description = request.POST['description']
    lc.district = getLocation(request.POST['district']).key()
    lc.sub_district = getLocation(request.POST['sub_district']).key()
    lc.village = getLocation(request.POST['village']).key()
    if request.POST['geo_pos']:
        lc.geo_pos = request.POST['geo_pos']
    lc.put()
    if not pid:
        counter.update('site_lc_count', 1)
    if 'photo' not in request.FILES:
        return lc
    save_file_upload(request, 'photo', lc)
    return lc 

def delete(request, pid=None):
    if not pid:
        return HttpResponseRedirect('/livecenter')
    item = db.get( pid )
    if not item:
        return HttpResponseRedirect('/livecenter')
    counter.update('site_lc_count', -1)
    item.delete()
    return HttpResponseRedirect('/livecenter')

def district(request, pid):
    json_data = []
    pid = int(pid)
    districts = LivelihoodLocation().all().order('dl_name').\
        filter('dl_parent = ', pid)
    for district in districts:
        json_data.append({
            'dl_id' : int(district.dl_id),
            'dl_name' : str(district.dl_name),
            'dl_key' : str(district.key())
            })
    return HttpResponse(json.encode(json_data))

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20
    if not Livelihood.objects.all()[:1]:
        Livelihood.counter_reset()
    offset = Livelihood.counter_value()
    sources = LiveCenter.all().order('__key__')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = Container.objects.filter(livecenter=str(source.key()))
        if target:
            continue
        target = Livelihood(name=source.name,
            address=source.address or '',
            description=source.description or '',
            geo_pos=source.geo_pos,
            updated=source.last_modified)
        for sc in source.category:
            c = CategoryContainer.objects.filter(livecategory=str(sc))[0].category
            target.category.append(c.id)
        target.district = Location.objects.filter(lid=source.district.dl_id)[0]
        target.sub_district = Location.objects.filter(lid=source.sub_district.dl_id)[0]
        target.village = Location.objects.filter(lid=source.village.dl_id)[0]
        photo = FileContainer.objects.filter(container=str(source.key()))[:1]
        if photo:
            target.photo = photo[0].file
        target.save()
        c = Container(livelihood=target, livecenter=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/livecenter.html', {
        'targets': targets, 
        })


############
# Category #
############
def category(request, pid):
    if request.POST:
        category_save(request, pid)
        return HttpResponseRedirect('/livecenter/show/%s' % pid)
    return direct_to_template(request, 'livecenter/category.html', {
        'livecenter': db.get(pid),
        'categories': LiveCategory.all().filter('no_ancestor', True),
        })

def category_save(request, pid):
    lc = db.get( pid )
    lc.category[:] = []
    for cat in request.POST.getlist('category'):
        lc.category.append(db.Key(cat))
    lc.save()

def category_migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(Category.objects.all())
    sources = LiveCategory.all().order('__key__')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = CategoryContainer.objects.filter(livecategory=str(source.key()))
        if target:
            continue
        target = Category(
            name=source.name,
            description=source.description,
            updated=source.last_modified)
        target.save()
        container = CategoryContainer(category=target,
            livecategory=str(source.key()))
        container.save()
        targets.append(target)
    if 'ancestor' in request.GET:
        for source in sources:
            if not source.ancestor:
                continue
            c = CategoryContainer.objects.filter(livecategory=str(source.key()))
            target = c[0].category
            target.ancestor = CategoryContainer.objects.filter(livecategory=str(source.ancestor[0]))[0].category
            target.save()
            targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/category.html', {
        'targets': targets, 
        })


###########
# Cluster #
###########
def cluster(request, pid):
    if request.POST:
        cluster_save(request, pid)
        return HttpResponseRedirect('/livecenter/show/%s' % pid)
    return direct_to_template(request, 'livecenter/cluster.html', {
        'livecenter': db.get(db.Key(pid)),
        'categories': LiveCategory.all().filter('no_ancestor', True),
        })
    
def cluster_save(request, pid):    
    item = LiveCluster()
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.category = db.Key(request.POST['category'])
    item.livecenter.append(db.Key(pid))
    item.put()
    save_file_upload(request, 'photo', item)

############
# Location #
############
def location_migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(Location.objects.all())
    sources = LivelihoodLocation.all().order('dl_id')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = Location.objects.filter(lid=source.dl_id)
        if target:
            continue
        target = Location(lid=source.dl_id,
            name=source.dl_name,
            parent=source.dl_parent)
        target.save()
        targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/location.html', {
        'targets': targets, 
        })


