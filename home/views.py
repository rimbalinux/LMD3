from django.views.generic.simple import direct_to_template


def index(request):
    return direct_to_template(request, 'home.html', {
        'lokasi': '4.038521855794782 96.9927978515625', 
        })
