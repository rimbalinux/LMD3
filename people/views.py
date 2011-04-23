from livecenter.models import Person, PersonTraining
from livecenter.views import DEFAULT_LOCATION
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, people, next = SearchablePagerQuery(Person).search(q).order('-last_modified').fetch(8, page)
    return direct_to_template(request, 'people/index.html', {
        'people': people,
        'people_count': counter.get('site_member_count'),
        'prev': prev,
        'next': next,
        'lokasi': ', '.join(map(lambda x: str(x), DEFAULT_LOCATION)),
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
        'lokasi': str(item.geo_pos).strip('nan,nan') or ', '.join(DEFAULT_LOCATION),
        })
