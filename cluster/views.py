from livecenter.models import LiveCluster, LiveGroup, LiveCategory, Cluster, Container, \
        ClusterContainer, CategoryContainer, LiveCenter
from attachment.utils import save_file_upload
from attachment.models import Container as FileContainer
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery

def edit(request, pid):
    if request.POST:
        save(request, pid)
        return HttpResponseRedirect(request.POST['destination'])
    return direct_to_template(request, 'cluster/edit.html', {
        'cluster': db.get(db.Key(pid)),
        'categories': LiveCategory.all(),
        'destination': 'destination' in request.GET and request.GET['destination'] or '/',
        })
    
def save(request, pid):    
    item = db.get(db.Key(pid))
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.category = db.Key(request.POST['category'])
    item.put()
    save_file_upload(request, 'photo', item)
    
def show(request, pid):
    item = db.get(db.Key(pid))
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, groups, next = SearchablePagerQuery(LiveGroup).\
        filter('livecluster =',item.key()).order('__key__').fetch(15, page)
    other_cluster = LiveCluster.all().order('__key__').\
                  filter('livecenter =', item.livecenter[0]).\
                  filter('__key__ !=', item.key()).fetch(5)
    return direct_to_template(request, 'cluster/show_group.html', {
        'groups': groups,
        'other_cluster':other_cluster,
        'cluster': item,
        'prev': prev,
        'next': next,
        })
    
def delete(request, pid):
    item = db.get(db.Key(pid))
    if item:
        item.delete()
    return HttpResponseRedirect(request.GET['destination'])

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20
    if not Cluster.objects.all()[:1]:
        Cluster.counter_reset()
    offset = Cluster.counter_value()
    sources = LiveCluster.all().order('__key__').\
        filter('__key__ !=', db.Key('ahlsaXZlbGlob29kbWVtYmVyc2RhdGFiYXNlchILEgtMaXZlQ2x1c3RlchjlNww')).\
        filter('__key__ !=', db.Key('ahlsaXZlbGlob29kbWVtYmVyc2RhdGFiYXNlchILEgtMaXZlQ2x1c3RlchjjTww'))
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = ClusterContainer.objects.filter(livecluster=str(source.key()))
        if target:
            continue
        target = Cluster(name=source.name,
            info=source.info or '',
            category=CategoryContainer.objects.filter(livecategory=str(source.category.key()))[0].category,
            livecenter=Container.objects.filter(livecenter=str(source.livecenter[0]))[0].livelihood)
        photo = FileContainer.objects.filter(container=str(source.key()))[:1]
        if photo:
            target.photo = photo[0].file
        target.save()
        c = ClusterContainer(cluster=target, livecluster=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'cluster/migrate.html', {
        'targets': targets, 
        })


