from django.http import HttpResponseRedirect

def lang(request, lang_id):
    request.session['lang'] = lang_id
    request.session.modified = True
    dest = 'destination' in request.GET and request.GET['destination'] or '/'
    return HttpResponseRedirect(dest)
