from .models import LiveCenter, MicroFinance, Person, LivelihoodLocation, \
        Attachment, LiveCluster, LiveCategory
from attachment.models import Attachment
from attachment.utils import save_file_upload
from .utils import getLocation
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter
import json


DEFAULT_LOCATION = [4.0287, 96.7181]

def default_location():
    return ', '.join(map(lambda x: str(x), DEFAULT_LOCATION))

def index(request):
    items = LiveCenter.all().order('name')
    return direct_to_template(request, 'livecenter/index.html', {
        'livecenters': items,
        'lokasi': default_location(), 
        })

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
    
def people(request, pid):
    if request.POST:
        people_save(request, pid)
        return HttpResponseRedirect('/livecenter/show/%s' % pid)
    return direct_to_template(request, 'livecenter/people.html', {
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        'livecenter': db.get(pid),
        'district_sel': 0,
        'subdistrict_sel': 0,
        'village_sel': 0,
        })

def people_save(request, pid):
    item = Person()
    item.name         = request.POST['name']
    item.description  = request.POST['description']
    item.district     = getLocation(request.POST['district']).key()
    item.sub_district = getLocation(request.POST['sub_district']).key()
    item.village      = getLocation(request.POST['village']).key()
    if request.POST['geo_pos']:
        item.geo_pos = request.POST['geo_pos']
    #item.livecenter   = db.Key(request.POST['livecenter'])
    item.livecenter   = db.Key(pid)
    item.gender       = request.POST['gender']
    item.birth_place  = request.POST['birth_place']
    item.education    = request.POST['education']
    item.spouse_name  = request.POST['spouse_name']
    item.member_type  = request.POST['member_type']
    item.info         = request.POST['info']
    if request.POST['address']:
        item.address  = request.POST['address']
    if request.POST['mobile']:
        item.mobile   = request.POST['mobile']
    if request.POST['email']:
        item.email    = request.POST['email']
    if request.POST['birth_year']:
        item.birth_year   = int(request.POST['birth_year'])
    if request.POST['monthly_income']:
        item.monthly_income = int(request.POST['monthly_income'])
    if request.POST['children_num']:
        item.children_num = int(request.POST['children_num'])
    item.put()
    counter.update('site_member_count', 1)
    counter.update('lc_member_count_%s' % item.livecenter.key().id(), 1)
    save_file_upload(request, 'photo', item)
    return item
