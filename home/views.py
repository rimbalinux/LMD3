from people.models import People
from livecenter.models import Livelihood
from django.views.generic.simple import direct_to_template
from livecenter.utils import default_location


def index(request):
    return direct_to_template(request, 'home.html', {
        'livecenters': Livelihood.objects.all().order_by('name'),
        'peoples': People.objects.filter(photo__isnull=False).order_by('-photo_id')[:20],
        'people_count': People.counter_value(),
        'lokasi': default_location(), 
        })
