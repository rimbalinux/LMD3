import urllib
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
import json
from authority.decorators import permission_required_or_403
from microfinance.models import Finance
from group.models import Group
from people.models import People
from product.models import Product
from .utils import default_location, redirect
from .models import Category, Livelihood, Location, Cluster, Metaform
from .forms import LivelihoodForm
#from .models import LiveCenter, MicroFinance, Person, LivelihoodLocation, \
#        LiveCluster, LiveCategory, MetaForm, \
#        CategoryContainer, Container, MetaformContainer
#from .utils import migrate_photo


def get_livecenters():
    lcs = []
    limit = 20
    offset = 0
    while True:
        found = False
        for lc in Livelihood.objects.all().order_by('name')[offset:offset+limit]:
            found = True
            if lc.allowed:
                lcs.append(lc)
                if len(lcs) == limit:
                    return lcs
        if not found:
            return lcs
        offset += limit

def index(request):
    return direct_to_template(request, 'livecenter/index.html', {
        'livecenters': get_livecenters(), 
        'count': Livelihood.counter_value(),
        'lokasi': default_location(), 
        })

def destination(lid, tabname):
    return urllib.quote('/livecenter/show/%s?tab=%s' % (lid, tabname))

def show(request, lid):
    lc = Livelihood.objects.get(pk=lid)
    related_lc = lc.category and \
            Livelihood.objects.filter(category__in=lc.category).\
            exclude(pk=lc.id) or None
    return direct_to_template(request, 'livecenter/show.html', {
        'livecenter': lc,
        'peoples': People.objects.order_by('-updated').filter(livecenter=lc),
        'clusters': Cluster.objects.order_by('name').filter(livecenter=lc),
        'groups': Group.objects.order_by('name').filter(livecenter=lc),
        'finances': Finance.objects.filter(district=lc.district),
        'related_livecenter': related_lc,
        'tab_member': destination(lid, 'member'),
        'tab_cluster': destination(lid, 'cluster'),
        'tab_group': destination(lid, 'group'),
        'lokasi': default_location(lc.geo_pos),
        })

def create(request):
    lc = Livelihood()
    return show_edit(request, lc) 

def edit(request, lid):
    lc = Livelihood.objects.get(pk=lid)
    return show_edit(request, lc)

@permission_required_or_403('livecenter.change_livelihood')
def show_edit(request, lc):
    form = LivelihoodForm(instance=lc)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/livecenter/show/%d' % lc.id)
    return direct_to_template(request, 'livecenter/edit.html', {
        'form': form,
        })

@permission_required_or_403('livecenter.change_livelihood')
def delete(request, lid):
    lc = Livelihood.objects.get(pk=lid)
    if request.POST:
        if 'delete' in request.POST:
            _delete(lc)
            return redirect(request, '/livecenter')
        return redirect(request, '/livecenter/show/%d' % lc.id)
    return direct_to_template(request, 'livecenter/delete.html', {
        'instance': lc,
        })

def _delete(lc):
    for member in People.objects.filter(livecenter=lc):
        for product in Product.objects.filter(person=member):
            product.delete()
        member.delete()
    for group in Group.objects.filter(livecenter=lc):
        group.delete()
    for cluster in Cluster.objects.filter(livecenter=lc):
        cluster.delete()
    lc.delete()

def district(request, pid):
    json_data = []
    if pid:
        loc = Location.objects.get(pk=pid)
        for district in Location.objects.order_by('name').\
                filter(parent=loc.lid):
            json_data.append({
                'id' : district.id,
                'name' : district.name,
                })
    return HttpResponse(json.encode(json_data))

"""
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
            geo_pos=str(source.geo_pos) != 'nan,nan' and str(source.geo_pos) or '',
            updated=source.last_modified)
        for sc in source.category:
            c = CategoryContainer.objects.filter(livecategory=str(sc))[0].category
            target.category.append(c.id)
        district = Location.objects.filter(lid=source.district.dl_id)[:1]
        target.district = district and district[0] or None
        sub_district = Location.objects.filter(lid=source.sub_district.dl_id)[:1]
        target.sub_district = sub_district and sub_district[0] or None
        village = Location.objects.filter(lid=source.village.dl_id)[:1]
        target.village = village and village[0] or None
        target.photo = migrate_photo(request, source)
        target.save()
        c = Container(livelihood=target, livecenter=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/livecenter.html', {
        'targets': targets, 
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Livelihood.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in Container.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'livecenter/migrate/livecenter.html', {
        'targets': targets, 
        })
"""


############
# Category #
############
"""
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
            updated=source.last_modified,
            photo=migrate_photo(request, source))
        target.save()
        container = CategoryContainer(category=target,
            livecategory=str(source.key()))
        container.save()
        targets.append(target)
    if not targets:
        for source in sources:
            if not source.ancestor:
                continue
            c = CategoryContainer.objects.filter(livecategory=str(source.key()))
            target = c[0].category
            if target.ancestor:
                continue
            target.ancestor = CategoryContainer.objects.filter(livecategory=str(source.ancestor[0]))[0].category
            target.save()
            targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/category.html', {
        'targets': targets, 
        })

def category_migrate_delete(request): # danger
    targets = []
    limit = 20
    for target in Category.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for cc in CategoryContainer.objects.all()[:limit]:
        cc.delete()
    return direct_to_template(request, 'livecenter/migrate/category.html', {
        'targets': targets, 
        })
"""

############
# Location #
############
"""
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

def location_migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Location.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    return direct_to_template(request, 'livecenter/migrate/location.html', {
        'targets': targets, 
        })
"""

############
# Metaform #
############
"""
def migrate_metaform(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(Metaform.objects.all())
    sources = MetaForm.all().order('__key__')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = MetaformContainer.objects.filter(old=source.key())
        if target:
            continue
        target = Metaform(title=source.title,
            meta_type=source.meta_type,
            category=CategoryContainer.objects.filter(livecategory=str(source.container[0]))[0].category,
            slug=source.slug,
            form_type=source.form_type,
            attribute=source.attribute,
            description=source.description)
        target.save()
        mc = MetaformContainer(new=target, old=str(source.key()))
        mc.save()
        targets.append(target)
    return direct_to_template(request, 'livecenter/migrate/metaform.html', {
        'targets': targets, 
        })

def migrate_metaform_delete(request): # danger
    targets = []
    for target in Metaform.objects.all()[:20]:
        targets.append(target)
        target.delete()
    for mc in MetaformContainer.objects.all()[:20]:
        mc.delete()
    return direct_to_template(request, 'livecenter/migrate/metaform.html', {
        'targets': targets, 
        })
"""
