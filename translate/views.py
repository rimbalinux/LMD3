from django.http import HttpResponseRedirect
from .models import Dictionary


def lang(request, lang_id):
    request.session['lang'] = lang_id
    request.session.modified = True
    dest = 'destination' in request.GET and request.GET['destination'] or '/'
    return HttpResponseRedirect(dest)

DICT = [
    ['Beranda', 'Home'],
    ]

def dictionary(request):
    for src, to in DICT:
        ds = Dictionary.objects.filter(
            input_lang='id',
            output_lang='en',
            input=src)[:1]
        if ds:
            continue
        d = Dictionary(input_lang='id',
                output_lang='en',
                input=src,
                output=to)
        d.save()
    return HttpResponseRedirect('/')

