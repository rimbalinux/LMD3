from .models import Product
from livecenter.models import LiveGroup, MetaForm
from livecenter.views import DEFAULT_LOCATION
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    #prev, product, next = SearchablePagerQuery(Product).search(q).fetch(8, page)
    product = Product.all()
    products = {}
    i = 0
    for p in product:
        i += 1
        name = p.name.upper().strip()
        if name in products:
            products[name] += 1
        else:
            products[name] = 1
    product_list = [] # nama, jumlah
    for name in products:
        product_list.append([name, products[name]])
    product_list.sort()
    return direct_to_template(request, 'product/index.html', {
        'product_list': product_list,
        'product_count': counter.get('site_product_count'),
        #'prev': prev,
        #'next': next,
        'lokasi': ', '.join(map(lambda x: str(x), DEFAULT_LOCATION)),
        })

def show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/product')
    return direct_to_template(request, 'product/show.html', {
        'customfields': MetaForm.all().order('__key__').filter('meta_type', 'product').filter('container', item.category.key()),
        'product': item,
        'person': item.person,
        'lokasi': str(item.geo_pos).strip('nan,nan') or ', '.join(DEFAULT_LOCATION),
        })
