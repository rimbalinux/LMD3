from .models import File
#from .models import Attachment, File, Container
#from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect
#from django.views.generic.simple import direct_to_template
#from livecenter.models import Person, LiveCluster
#from product.models import Product
#import counter


def default():
    return HttpResponseRedirect('/images/default.gif')

def image(request, fid):
    if not fid:
        return default()
    image = File.objects.get(pk=fid)
    response = HttpResponse(mimetype=image.mime)
    response.write(image.content)
    return response

def delete(request, fid):
    image = File.objects.get(pk=fid)
    image.delete()
    return default()


"""
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

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = counter.get('attachment_file')
    sources = Attachment.all().order('filename')
    kinds = {}
    total_bytes = 0
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        if not source.containers:
            continue
        target = File.objects.filter(name=source.filename)
        if target:
            continue
        byte = len(source.file)
        total_bytes += byte
        target = File(name=source.filename, content=source.file,
            mime='image/png', size=byte, user=request.user)
        target.save()
        c = Container(file=target, container=source.containers[0])
        c.save()
        counter.update('attachment_file', 1)
        targets.append([target, c])
        kind = c.container.kind()
        if kind in kinds:
            kinds[kind] += 1
        else:
            kinds[kind] = 0
    return direct_to_template(request, 'attachment/migrate.html', {
        'targets': targets, 
        'example': targets and targets[0][0],
        'kinds': kinds,
        'total_bytes': total_bytes,
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in File.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    temp = []
    for c in Container.objects.all()[:limit]:
        temp.append(c)
        c.delete()
    return direct_to_template(request, 'attachment/migrate.html', {
        'targets': targets,
        'temps': temp,
        })

"""
