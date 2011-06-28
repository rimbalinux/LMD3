import re
from google.appengine.ext import db
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from authority.decorators import permission_required_or_403
from livecenter.utils import default_location, redirect
from livecenter.models import Metaform
from people.models import People
from .models import Product, Type
from .forms import ProductForm, TypeForm
#from livecenter.utils import migrate_photo
#from .models import Container
#from people.models import Container as PersonContainer
#from livecenter.models import LiveGroup, Product as OldProduct, \
#        CategoryContainer, ClusterContainer

# migrasi
"""
pola = [
        ['^tuna|^nelayan|^pedagang','Tuna'],
        ['^bandeng|^ikan bandeng|^buruh tambak','Bandeng'],
        ['^udang','Udang'],
        ['^lele|^ikan lele|^pembenihan ikan lele','Lele'],
        ['^nilam','Nilam'],
        ['^nila$|^nila |^ikan nila','Nila'],
        ['^mujaer|^ikan mujaer','Mujair'],
        ['^gurami','Gurami'],
        ['^ikan asin|^asin peda|^teri nasi','Ikan Asin'],
        ['^ikan bawal','Bawal'],
        ['^ikan mas','Ikan Mas'],
        ['^ikan patin','Patin'],
        ['^ikan rambe','Ikan Rambai'], 
        ['^pembuat perahu','Perahu'],
        ['^tiram|^pencari tiram','Tiram'],
        ['^tripang','Tripang'],
        ['^kepiting lunak','Kepiting Lunak'],
        ['^k macan','Kepiting Macan'],
        ['^coklat|^nasri','Coklat'],
       ]
"""


def index(request):
    return direct_to_template(request, 'product/index.html', {
        'types': Type.objects.all().order_by('-count','name'),
        'products': Product.objects.exclude(geo_pos='')[:1000],
        'count': Product.counter_value(),
        'lokasi': default_location(),
        })

def show(request, pid):
    product = Product.objects.get(pk=pid)
    return direct_to_template(request, 'product/show.html', {
        'customfields': Metaform.objects.filter(meta_type='product').\
                filter(category=product.category),
        'product': product, 
        'lokasi': default_location(product.geo_pos), 
        })

def create(request, pid): # person id
    person = People.objects.get(pk=pid)
    product = Product(person=person,
        livecenter=person.livecenter)
    return show_edit(request, product)

def edit(request, pid): # product id
    product = Product.objects.get(pk=pid)
    return show_edit(request, product)
 
@permission_required_or_403('product.change_product')
def show_edit(request, product):
    form = ProductForm(instance=product)
    if request.POST:
        if 'delete' in request.POST:
            product.delete()
            return redirect(request, '/product')
        if form.is_valid():
            form.save()
            return redirect(request, '/product/show/%d' % product.id)
    return direct_to_template(request, 'product/edit.html', {
        'form': form, 
        })

def type_show(request, tid):
    limit = 20
    page = 'page' in request.GET and int(request.GET['page']) or 1
    offset = page * limit - limit
    products = []
    q = Product.objects.filter(type=tid).order_by('-updated')
    for product in q[offset:offset+limit]:
        if product.allowed:
            products.append(product)
    return direct_to_template(request, 'product/type/show.html', {
        'product_type': Type.objects.get(pk=tid),
        'products': products, 
        'lokasi': default_location(), 
        })

def type_create(request):
    return type_show_edit(request, Type())

def type_edit(request, tid):
    type_ = Type.objects.get(pk=tid)
    return type_show_edit(request, type_)

def type_show_edit(request, type_):
    form = TypeForm(instance=type_)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request, '/product/type/%d' % type_.id)
    return direct_to_template(request, 'product/type/edit.html', {
        'form': form,
        })

"""
def migrate(request):
    def intval(n):
        try:
            return int(n)
        except ValueError:
            return

    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(Product.objects.all())
    sources = OldProduct.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = Container.objects.filter(old=str(source.key()))
        if target:
            continue
        try:
            person_key = str(source.person.key())
        except db.ReferencePropertyResolveError, e:
            errors.append(e)
            continue
        person = PersonContainer.objects.filter(person=person_key)[:1]
        #if not person:
        #    continue
        person = person[0]
        target = Product(
            name=source.name,
            category=CategoryContainer.objects.filter(livecategory=str(source.category.key()))[0].category,
            person=person.people,
            geo_pos=str(source.geo_pos) != 'nan,nan' and source.geo_pos or '',
            info=source.info,
            year=intval(source.year),
            photo=migrate_photo(request, source))
        name_ = target.name.lower()
        type_ = None
        for cari, key in pola:
            if re.compile(cari).search(name_):
                target.type = type_ = Type.objects.get(name=key)
                break
        if not type_:
            raise Exception('%s belum ditemukan tipenya' % name_)
        target.save()
        c = Container(new=target, old=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'product/migrate.html', {
        'targets': targets,
        'errors': errors,
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Product.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in Container.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'product/migrate.html', {
        'targets': targets, 
        })


def types(request):
    if not Type.objects.all()[:1]:
        for regex, name in pola:
            t = Type(name=name, user=request.user)
            t.save()
    return direct_to_template(request, 'product/type/created.html', {
        'targets': Type.objects.all(),
        })
"""
