from .models import LiveCenter 
from django.views.generic.simple import direct_to_template


def index(request):
    items = LiveCenter.all().order('name')
    return direct_to_template(request, 'index.html', {
        'livecenters': items,
        'lokasi': '4.0287, 96.7181',
        'debug': dir(items),
        })
