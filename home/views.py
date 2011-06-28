from people.models import People
from livecenter.models import Livelihood
from django.views.generic.simple import direct_to_template
from livecenter.utils import default_location


def index(request):
    limit = 20
    page = 'page' in request.GET and int(request.GET['page']) or 1
    offset = page * limit - limit
    lcs = []
    q = Livelihood.objects.all().order_by('name')
    for lc in q[offset:offset+limit]:
        if lc.allowed:
            lcs.append(lc)
    return direct_to_template(request, 'home.html', {
        'livecenters': lcs, 
        'peoples': People.objects.filter(photo__isnull=False).order_by('-photo_id')[:20],
        'people_count': People.counter_value(),
        'lokasi': default_location(), 
        })
