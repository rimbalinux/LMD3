import urllib
from google.appengine.ext import db
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import counter
from livecenter.models import Person, PersonTraining, LivelihoodLocation, \
        LiveCenter, Container, Location, Metaform, Livelihood
from livecenter.utils import redirect, default_location, migrate_photo
from product.models import Product
from group.models import Group, Container as GroupContainer
from attachment.utils import save_file_upload
from transaction.models import Transaction
from .models import People, Container as PeopleContainer, Training
from .settings import GENDERS
from .forms import PeopleForm


def index(request):
    return direct_to_template(request, 'people/index.html', {
        'peoples': People.objects.all().order_by('-updated'),
        #'positions': People.objects.all().exclude(geo_pos='').order_by('-updated'),
        'count': People.counter_value(),
        'lokasi': default_location(),
        })

def destination(pid, tabname):
    return urllib.quote('/people/show/%s?tab=%s' % (pid, tabname))

def show(request, pid):
    try:
        people = People.objects.get(id=pid)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/people')
    customfields = boat = None 
    if people.group and people.group.cluster.category.name.upper() == 'CAPTURE FISHERIES':
        customfields = Metaform.objects.order_by('id').\
            filter(category=people.group.cluster.category).\
            filter(meta_type='group')
        boat = people.group
    return direct_to_template(request, 'people/show.html', {
        'person': people,
        'boat': boat,
        'customfields': customfields,
        'trainings': Training.objects.filter(person=people),
        'transactions': Transaction.objects.filter(person=people),
        'products': Product.objects.filter(person=people),
        'tab_product': destination(people.id, 'product'),
        'tab_transaction': destination(people.id, 'transaction'),
        'lokasi': default_location(people.geo_pos),
        })

def create(request, lid): # lid = livecenter id 
    lc = Livelihood.objects.get(pk=lid)
    person = People(livecenter=lc)
    return show_edit(request, person)

def edit(request, pid): # pid = people id
    person = People.objects.get(pk=pid)
    return show_edit(request, person)
 
def show_edit(request, person):
    form = PeopleForm(instance=person)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request, '/people/show/%d' % person.id)
    return direct_to_template(request, 'people/edit.html', {
        'form': form, 
        })

def delete(request, pid):
    p = People.objects.get(pk=pid)
    p.delete()
    return redirect(request, '/people')

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(People.objects.all())
    sources = Person.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = PeopleContainer.objects.filter(person=str(source.key()))
        if target:
            continue
        try:
            livecenter_key = str(source.livecenter.key())
        except db.ReferencePropertyResolveError, e:
            errors.append(e)
            continue
        target = People(
            name=source.name,
            livecenter=Container.objects.filter(livecenter=livecenter_key)[0].livelihood,
            email=source.email or '',
            gender=source.gender=='Male',
            birth_year=source.birth_year,
            birth_place=source.birth_place or '',
            address=source.address and source.address != 'None' and source.address or '',
            village=source.village and Location.objects.filter(lid=source.village.dl_id)[0] or None,
            sub_district=source.sub_district and Location.objects.filter(lid=source.sub_district.dl_id)[0] or None,
            district=source.district and Location.objects.filter(lid=source.district.dl_id)[0] or None,
            education=source.education or '',
            spouse_name=source.spouse_name and source.spouse_name != '0' and source.spouse_name or '',
            monthly_income=source.monthly_income,
            children_num=source.children_num,
            member_type=source.member_type or '',
            mobile=source.mobile and source.mobile != '0' and source.mobile or '',
            info=source.info or '',
            geo_pos=str(source.geo_pos) != 'nan,nan' and source.geo_pos or '')
        target.geo_pos = target.geo_pos == '0.0,0.0' and None
        if source.livegroup:
            c = GroupContainer.objects.filter(livegroup=str(source.livegroup[0]))[:1]
            if c:
                target.group = c[0].group
        target.photo = migrate_photo(request, source)
        target.save()
        c = PeopleContainer(people=target, person=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'people/migrate.html', {
        'targets': targets,
        'errors': errors,
        })

def migrate_delete(request): # danger
    targets = []
    limit = 20 
    for target in People.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for pc in PeopleContainer.objects.all()[:limit]:
        pc.delete()
    return direct_to_template(request, 'people/migrate.html', {
        'targets': targets, 
        })


# Hitung ulang jumlah anggota pada suatu livecenter. Sebelum fungsi ini
# dipanggil, pastikan seluruh field member_count = 0 pada tabel
# livecenter_livelihood.
def repair_livecenter_member_count(request):
    counter_name = '__livecenter_member_count_offset'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.order_by('id')[offset:20]:
        people.livecenter.member_count += 1
        people.livecenter.save()
        counter.increment(counter_name)
        targets.append(people)
    return direct_to_template(request, 'people/repair/livecenter_member_count.html', {
        'targets': targets,
        })

# Cari yang lokasinya sudah tidak ada
def location_not_found(request):
    for person in Person.all().filter('district', db.Key('ahlsaXZlbGlob29kbWVtYmVyc2RhdGFiYXNlchoLEhJMaXZlbGlob29kTG9jYXRpb24YhpICDA')):
        person.district = None
        person.put()
    return direct_to_template(request, 'people/location_not_found.html', {
        'targets': Person.all().filter('district', db.Key('ahlsaXZlbGlob29kbWVtYmVyc2RhdGFiYXNlchoLEhJMaXZlbGlob29kTG9jYXRpb24YhpICDA')),
        })

# Hitung ulang jumlah anggota pada suatu group. Sebelum fungsi ini
# dipanggil, pastikan seluruh field member_count = 0 pada tabel
# group_group.
def repair_group_member_count(request):
    counter_name = '__group_member_count_offset'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.order_by('id')[offset:offset+20]:
        targets.append(people)
        if not people.group:
            continue
        people.group.member_count += 1
        people.group.save()
        counter.increment(counter_name)
    return direct_to_template(request, 'people/repair/group_member_count.html', {
        'targets': targets,
        })

# Ubah geo_pos = 0.0,0.0 menjadi string hampa.
def repair_geo_pos(request):
    counter_name = '__people_geo_pos_repair'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.filter(geo_pos='0.0,0.0').order_by('id')[offset:offset+20]:
        targets.append(people)
        people.geo_pos = ''
        people.save()
        counter.increment(counter_name)
    return direct_to_template(request, 'people/repair/geo_pos.html', {
        'targets': targets,
        })

# Ubah mobile = 0 menjadi string hampa.
def repair_mobile(request):
    counter_name = '__people_mobile_repair'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.filter(mobile='0').order_by('id')[offset:offset+20]:
        targets.append(people)
        people.mobile = ''
        people.save()
        counter.increment(counter_name)
    return direct_to_template(request, 'people/repair/mobile.html', {
        'targets': targets,
        })

# Ubah address = None menjadi string hampa.
def repair_address(request):
    counter_name = '__people_address_repair'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.order_by('id')[offset:offset+20]:
        counter.increment(counter_name)
        if people.address == 'None':
            continue
        targets.append(people)
        people.address = ''
        people.save()
    return direct_to_template(request, 'people/repair/address.html', {
        'targets': targets,
        })

# Ubah monthly_income = 0 menjadi string hampa.
def repair_monthly_income(request):
    counter_name = '__people_monthly_income_repair'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.filter(monthly_income=0).order_by('id')[offset:offset+20]:
        targets.append(people)
        people.monthly_income = None
        people.save()
        counter.increment(counter_name)
    return direct_to_template(request, 'people/repair/monthly_income.html', {
        'targets': targets,
        })

# Ubah spouse_name = 0 menjadi string hampa.
def repair_spouse_name(request):
    counter_name = '__people_spouse_name_repair'
    offset = counter.get(counter_name)
    targets = []
    for people in People.objects.filter(spouse_name='0').order_by('name')[offset:offset+20]:
        targets.append(people)
        people.spouse_name = '' 
        people.save()
        counter.increment(counter_name)
    return direct_to_template(request, 'people/repair/spouse_name.html', {
        'targets': targets,
        })

