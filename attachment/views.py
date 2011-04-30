from .models import Attachment 
from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from livecenter.models import Person, LiveCluster
from product.models import Product


def image(request, fid):
    response = HttpResponse(mimetype='image/png')
    image = Attachment.all().filter('containers = ', db.Key(fid)).get()
    if image:
        response.write(image.file)
        return response
    return HttpResponseRedirect('/images/default.gif')

def imgid(request, fid):
    image = Attachment.all().filter('__key__ = ', db.Key(fid)).get()
    if image:
        response = HttpResponse(mimetype='image/png')
        response.write(image.file)
        return response
    return HttpResponseRedirect('/images/default.gif')

def _delete(fid):
    image = Attachment.all().filter('__key__ = ', db.Key(fid)).get()
    if image:
        image.delete()

def delete(request, fid):
    _delete(fid)
    return HttpResponseRedirect('/img/no-container')

def delete_form(request):
    if 'delete_checked' in request.POST:
        for fid in request.POST.getlist('fid'):
            _delete(fid)
    elif 'delete_all' in request.POST:
        atts, container_kinds, total_bytes = delete_candidates()
        for att, containers in atts:
            _delete(str(att.key()))

def delete_candidates():
    atts = []
    total_bytes = 0
    container_kinds = {}
    for att in Attachment.all().fetch(1000):
        containers = []
        for container in att.containers:
            item = db.get(container)
            if item:
                continue
            kind = container.kind()
            if kind == 'Person':
                url_check = '/people/show/%s' % container
            elif kind == 'LiveCluster':
                url_check = '/cluster/edit/%s' % container
            else:
                url_check = ''
            containers.append([container, url_check])
            if kind in container_kinds:
                container_kinds[kind] += 1
            else:
                container_kinds[kind] = 1
        if containers:
            atts.append([att, containers])
            total_bytes += len(att.file)
    return atts, container_kinds, total_bytes 

def no_container(request):
    if request.POST:
        delete_form(request)
    atts, container_kinds, total_bytes = delete_candidates()
    limit = 20
    total_files = len(atts)
    return direct_to_template(request, 'attachment/no-container.html', {
        'atts': atts[:limit],
        'sisa': total_files > limit and total_files-limit or 0,
        'total_files': total_files, 
        'total_bytes': total_bytes,
        'kinds': container_kinds,
        })
