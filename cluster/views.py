from livecenter.models import LiveCluster, Cluster, Container, \
        ClusterContainer, CategoryContainer, Livelihood
from livecenter.utils import redirect, migrate_photo
from .forms import ClusterForm
from attachment.utils import save_file_upload
from django.views.generic.simple import direct_to_template
from google.appengine.ext import db


def create(request, lid): # add cluster
    lc = Livelihood.objects.get(pk=lid)
    cl = Cluster(livecenter=lc)
    return show(request, cl)

def edit(request, cid):
    cl = Cluster.objects.get(pk=cid)
    return show(request, cl)
 
def show(request, cl):
    if request.POST:
        form = ClusterForm(instance=cl.id and cl or None)
        if form.is_valid():
            form.save()
            return redirect(request)
    else:
        form = ClusterForm(instance=cl)
    return direct_to_template(request, 'cluster/edit.html', {
        'form': form,
        })

def delete(request, cid):
    cl = Cluster.objects.get(pk=cid)
    cl.delete()
    return redirect(request) 

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
            livecenter=Container.objects.filter(livecenter=str(source.livecenter[0]))[0].livelihood,
            photo=migrate_photo(request, source))
        target.save()
        c = ClusterContainer(cluster=target, livecluster=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'cluster/migrate.html', {
        'targets': targets, 
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Cluster.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in ClusterContainer.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'cluster/migrate.html', {
        'targets': targets, 
        })


