from livecenter.models import Person
from django.views.generic.simple import direct_to_template
from tipfy.pager import PagerQuery, SearchablePagerQuery


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, people, next = SearchablePagerQuery(Person).search(q).order('-last_modified').fetch(8, page)
    return direct_to_template(request, 'home.html', {
        'people': people,
        'prev': prev,
        'next': next,
        'lokasi': '4.038521855794782 96.9927978515625', 
        })
