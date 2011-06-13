from django.views.generic.simple import direct_to_template
from livecenter.models import Cluster, Livelihood
from livecenter.utils import redirect
from group.models import Group
from product.models import Product
from .forms import ClusterForm
#from google.appengine.ext import db
#from livecenter.utils import redirect, migrate_photo
#from livecenter.models import LiveCluster, Container, \
#        ClusterContainer, CategoryContainer


def create(request, lid): # add cluster
    lc = Livelihood.objects.get(pk=lid)
    cl = Cluster(livecenter=lc)
    return show(request, cl)

def edit(request, cid):
    cl = Cluster.objects.get(pk=cid)
    return show(request, cl)
 
def show(request, cl):
    form = ClusterForm(instance=cl)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request)
    return direct_to_template(request, 'cluster/edit.html', {
        'form': form,
        })

def delete(request, cid):
    cluster = Cluster.objects.get(pk=cid)
    if request.POST:
        if 'delete' in request.POST:
            _delete(cluster)
        return redirect(request, '/livecenter/show/%d?tab=cluster' % cluster.livecenter.id)
    return direct_to_template(request, 'cluster/delete.html', {
        'instance': cluster,
        'groups': Group.objects.filter(cluster=cluster),
        })

def _delete(cluster):
    for group in Group.objects.filter(cluster=cluster):
        group.cluster = None
        group.save()
    for product in Group.objects.filter(cluster=cluster):
        product.cluster = None
        product.save()
    cluster.delete()


"""
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
"""


