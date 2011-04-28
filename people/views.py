from livecenter.models import Person, PersonTraining, LivelihoodLocation, \
        LiveCenter
from livecenter.views import default_location 
from livecenter.utils import redirect, getLocationKey
from attachment.utils import save_file_upload
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


GENDERS = ['Male','Female']

def counter_update(lid, i):
    counter.update('site_member_count', i)
    counter.update('lc_member_count_%s' % lid, i)

def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, people, next = SearchablePagerQuery(Person).search(q).order('-last_modified').fetch(8, page)
    return direct_to_template(request, 'people/index.html', {
        'people': people,
        'people_count': counter.get('site_member_count'),
        'prev': prev,
        'next': next,
        'lokasi': default_location(), 
        })

def show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/people')
    customfields = boat = None 
    if item.groups:
        for group in item.groups:
            if group.livecluster.category.name.upper() == 'CAPTURE FISHERIES':
                customfields = MetaForm.all().order('__key__').\
                        filter('container', group.livecluster.category.key()).\
                        filter('meta_type', 'group').all()
                boat = group
    return direct_to_template(request, 'people/show.html', {
        'person': item,
        'boat': boat,
        'customfields': customfields,
        'training': PersonTraining.all().filter('person', item.key()),
        'lokasi': str(item.geo_pos).strip('nan,nan') or default_location(),
        })

def create(request, lid): # lid = livecenter
    if request.POST:
        item = Person()
        item.livecenter = db.Key(lid)
        save(request, item)
        return redirect(request, '/people/show/%s' % item.key())
    return direct_to_template(request, 'people/edit.html', {
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        'livecenter': db.get(lid),
        'district_sel': 0,
        'subdistrict_sel': 0,
        'village_sel': 0,
        'genders': GENDERS,
        })
 
def edit(request, pid): # pid = person id
    item = db.get(pid)
    if not item: # sudah dihapus
        return redirect(request, '/people')
    if request.POST:
        save(request, item)
        return redirect(request, '/people/show/%s' % pid)
    return direct_to_template(request, 'people/edit.html', {
        'person': item,
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        'livecenter': item.livecenter, 
        'district_sel': item.district.dl_id,
        'subdistrict_sel': item.sub_district.dl_id,
        'village_sel': item.village.dl_id,
        'genders': GENDERS,
        })

def save(request, item):
    item.name = request.POST['name']
    item.description = request.POST['description']
    if request.POST['district']:
        item.district = getLocationKey(request.POST['district'])
    if request.POST['sub_district']:
        item.sub_district = getLocationKey(request.POST['sub_district'])
    if request.POST['village']:
        item.village = getLocationKey(request.POST['village']).key()
    if request.POST['geo_pos']:
        item.geo_pos = request.POST['geo_pos']
    item.gender       = request.POST['gender']
    item.birth_place  = request.POST['birth_place']
    item.education    = request.POST['education']
    item.spouse_name  = request.POST['spouse_name']
    item.member_type  = request.POST['member_type']
    item.info         = request.POST['description']
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
    counter_update(item.livecenter.key().id(), 1)
    save_file_upload(request, 'photo', item)

def delete(request, pid):
    item = db.get(pid)
    if item:
        item.delete()
        counter_update(item.livecenter.key().id(), -1)
    return redirect(request, '/people')

def group(request, pid):
    if request.POST:
        group_save(request, pid)
        return HttpResponseRedirect('/people/%s' % pid)
    return direct_to_template(request, 'people/group.html', {
        'person': db.get(pid),
        })
    
def group_save(request, pid):
    person = db.get( pid )
    person.livegroup[:] = []
    for item in request.POST['group'].getlist():
        person.livegroup.append(db.Key(item))
    person.save()
