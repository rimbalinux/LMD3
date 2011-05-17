from livecenter.models import Person, PersonTraining, LivelihoodLocation, \
        LiveCenter, Container, Location
from .models import People, Container as PeopleContainer
from group.models import Group, Container as GroupContainer
from attachment.models import Container as FileContainer
from livecenter.utils import redirect, getLocationKey, default_location
from attachment.utils import save_file_upload
from transaction.models import Transaction
from .settings import GENDERS
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


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
        'transactions': Transaction.objects.filter(person=str(item.key())),
        'tab_transaction': '/people/show/%s?tab=transaction' % item.key(),
        'lokasi': default_location(item.geo_pos),
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
        'district_sel': item.district and item.district.dl_id or 0,
        'subdistrict_sel': item.sub_district and item.sub_district.dl_id or 0,
        'village_sel': item.village and item.village.dl_id or 0,
        'genders': GENDERS,
        'geo_pos': item.geo_pos,
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

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(People.objects.all())
    sources = Person.all().order('__key__')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = PeopleContainer.objects.filter(person=str(source.key()))
        if target:
            continue
        target = People(
            name=source.name,
            livecenter=Container.objects.filter(livecenter=str(source.livecenter.key()))[0].livelihood,
            email=source.email or '',
            gender=source.gender=='Male',
            birth_year=source.birth_year,
            birth_place=source.birth_place or '',
            address=source.address or '',
            village=Location.objects.filter(lid=source.village.dl_id)[0],
            sub_district=Location.objects.filter(lid=source.sub_district.dl_id)[0],
            district=Location.objects.filter(lid=source.district.dl_id)[0],
            education=source.education or '',
            spouse_name=source.spouse_name or '',
            monthly_income=source.monthly_income,
            children_num=source.children_num,
            member_type=source.member_type or '',
            mobile=source.mobile or '',
            info=source.info or '',
            geo_pos=source.geo_pos or '')
        if source.livegroup:
            c = GroupContainer.objects.filter(livegroup=str(source.livegroup[0]))[:1]
            if c:
                target.group = c[0].group
        photo = FileContainer.objects.filter(container=str(source.key()))[:1]
        if photo:
            target.photo = photo[0].file
        target.save()
        c = PeopleContainer(people=target, person=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'people/migrate.html', {
        'targets': targets, 
        })

