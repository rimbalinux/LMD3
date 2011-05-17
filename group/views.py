from livecenter.models import LiveGroup, LiveCenter, MetaForm, Report_Group, \
        GroupTraining, LiveCluster, Container, ClusterContainer
from .models import Group, Container as GroupContainer
from livecenter.utils import redirect, default_location
from attachment.utils import save_file_upload
from attachment.models import Container as FileContainer
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter
import urllib


def destination(pid, tabname):
    return urllib.quote('/group/show/%s?tab=%s' % (pid, tabname))

def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, group, next = SearchablePagerQuery(LiveGroup).\
            search(q).fetch(8, page)
    return direct_to_template(request, 'group/index.html', {
        'groups': group,
        'groups_count': counter.get('site_group_count'),
        'prev': prev,
        'next': next,
        'lokasi': default_location(), 
        })

def map(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/group')
    category = item.livecluster.category
    return direct_to_template(request, 'group/map_member.html', {
        'groups': item.members,
        'member_count': item.members.count(),
        'lokasi': str(item.geo_pos).strip('nan,nan') or ', '.join(DEFAULT_LOCATION),
        })

def show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/group')
    category = item.livecluster.category
    return direct_to_template(request, 'group/show.html', {
        'group': item,
        'member_count': item.members.count(),
        'livecenter': LiveCenter.all().filter('__key__', item.livecluster.livecenter[0]).get(),
        'other_groups': LiveGroup.all().filter('livecluster', item.livecluster ).filter('__key__ !=', item.key()),
        'customfields': MetaForm.all().order('__key__').filter('container', category.key()).filter('meta_type', 'group'),
        'report': Report_Group.all().filter('livecluster', item.livecluster ).filter('name_group', item.key()),
        'training': GroupTraining.all().filter('group', item.key()),
        'lokasi': str(item.geo_pos).strip('nan,nan') or default_location(),
        })

def report_show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/group')
    category = item.livecluster.category
    return direct_to_template(request, 'group/report_show.html', {
        'report': item,
        'customfields': MetaForm.all().order('__key__').filter('container', category.key()).filter('meta_type', 'group'),
        'lokasi': str(item.name_group.geo_pos).strip('nan,nan') or ', '.join(DEFAULT_LOCATION),
        'livecenter': LiveCenter.all().filter('__key__', item.name_group.livecluster.livecenter[0]).get(),
        })       

def report_delete(request, pid):
    item = db.get(pid)
    if item:
        group = item.name_group.key()
        item.delete()
        return redirect(request, '/group/show/%s?tab=laporan' % group)
    return redirect(request, '/group')
 
def edit(request, pid):
    if request.POST:
        group = save(request, pid)
        if group:
            return redirect(request, '/group/show/%s?tab=keterangan' % group.key())
        return HttpResponseRedirect('/group')
    group = db.get(pid)
    category = group.livecluster.category
    clusters = LiveCluster.all().filter('livecenter', group.livecluster.livecenter[0]).filter('category', category.key()).fetch(100)
    customfields = MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()).fetch(100)
    return direct_to_template(request, 'group/edit.html', {
        'group': group,
        'geo_pos': group.geo_pos,
        'category': category,
        'cluster': clusters,
        'customfields': customfields,
        })

def add_report(request, pid):
    if request.POST:
        group = save_report(request, pid)
        if group:
            return HttpResponseRedirect('/group/show/%s' % pid)
        return HttpResponseRedirect('/group')
    group = db.get(pid)
    category = group.livecluster.category
    clusters = LiveCluster.all().filter('livecenter', group.livecluster.livecenter[0]).filter('category', category.key()).fetch(100)
    customfields = MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()).fetch(100)
    return direct_to_template(request, 'group/add_report.html', {
        'group': group,
        'category': category,
        'cluster': clusters,
        'customfields': customfields,
        })

def add_training(request, pid):
    if request.POST:
        training = save_training(request, pid, 'create')
        if training:
            return HttpResponseRedirect('/group/show/%s' % pid)
        return HttpResponseRedirect('/group')
    group = db.get(pid)
    return direct_to_template(request, 'group/add_training.html', {
        'pagetitle': 'Tambah Pelatihan ' + group.name,
        'groups': group,
        'training': GroupTraining.all().filter('group =', group.key()),
        'urls': '/group/add_training/',
        })

def edit_training(request, pid):
    if request.POST:
        training = save_training(request, pid, 'edit')
        if training:
            return redirect(request, '/group/show/%s?tab=pelatihan' % training.group.key())
        return HttpResponseRedirect('/group')
    training = db.get(pid)
    return direct_to_template(request, 'group/add_training.html', {
        'pagetitle': 'Ubah Pelatihan ' + training.group.name,
        'groups': training,
        'training': GroupTraining.all().filter('group =', training.group.key()),
        'urls': '/group/edit_training/',
        })

def edit_report(request, pid):
    if request.POST:
        group = save_edit_report(request, pid)
        if group:
            return HttpResponseRedirect('/group/report_show/%s' % pid)
        return HttpResponseRedirect('/group')
    group = db.get(pid)
    category = group.livecluster.category
    return direct_to_template(request, 'group/edit_report.html', {
        'pagetitle': 'Edit Report ' + group.name,
        'group': group,
        'category': category,
        'cluster': LiveCluster.all().filter('livecenter', group.livecluster.livecenter[0]).filter('category', category.key()),
        'customfields': MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()),
        })
 
def create(request, lid, cid):
    lc = db.get(db.Key(lid))
    cluster = db.get(db.Key(cid))
    customfields = MetaForm.all().order('__key__').\
            filter('meta_type', 'group').\
            filter('container', cluster.category.key())
    if request.POST:
        save(request, lc, cluster, customfields)
        return redirect(request, '/group')
    category = cluster.category
    return direct_to_template(request, 'group/create.html', {
        'livecenter': lc,
        'cluster': cluster,
        'clusters': LiveCluster.all().filter('livecenter', lc.key()).\
                filter('category', category.key()),
        'customfields': customfields,
        })

def save(request, pid=None):
    if pid:
        group = db.get(pid)
        if not group:
            return
    else:
        group = LiveGroup()
    group = db.get(pid)
    category = group.livecluster.category
    customfields = MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()).fetch(100)
    group.livecluster = db.Key(request.POST['cluster'])
    group.name = request.POST['name']
    group.info = request.POST['info']
    if request.POST['geo_pos']:
        group.geo_pos = request.POST['geo_pos']
    group.put()
    for meta in customfields:
        if request.POST[meta.slug]:
            try:
                if meta.form_type == 'file':
                    if not request.POST[meta.slug]:
                        continue
                    val = db.Blob(request.POST[meta.slug])
                    setattr(group, meta.slug, val)
                else:
                    setattr(group, meta.slug, request.POST[meta.slug])
            except: pass
    group.put()
    if not pid:
        counter.update('site_group_count', 1)
    if 'photo' not in request.FILES:
        return group
    save_file_upload(request, 'photo', lc)
    return group

def save_report(request, pid=None):
    item = db.get(pid)
    lc_key =  item.livecluster.livecenter[0]
    lc = db.get(lc_key)
    category = item.livecluster.category
    customfields = MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()).fetch(100)
    item = Report_Group()
    item.name_group = db.Key(request.POST['name_key'])
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.livecluster = db.Key(request.POST['cluster'])
    item.containers.append(lc.key())
    if request.POST['date']:
        item.year = request.POST['date']
    item.put()
    metas = {}
    for meta in customfields:
        if request.POST[meta.slug]:
            try:
                if meta.form_type == 'file':
                    if not request.POST[meta.slug]:
                        continue
                    val = db.Blob(request.POST[meta.slug])
                    setattr(item, meta.slug, val)
                else:
                    setattr(item, meta.slug, request.POST[meta.slug])
            except: pass
    item.put()
    return item

def save_edit_report(request, pid=None):
    item = db.get(pid)
    lc_key =  item.livecluster.livecenter[0]
    lc = db.get(lc_key)
    category = item.livecluster.category
    customfields = MetaForm.all().order('title').filter('meta_type', 'group').filter('container', category.key()).fetch(100)
    item.name_group = db.Key(request.POST['name_key'])
    item.name = request.POST['name']
    item.info = request.POST['info']
    item.livecluster = db.Key(request.POST['cluster'])
    if request.POST['date']:
        item.year = request.POST['date']
    item.put()

    for meta in customfields:
        if request.POST[meta.slug]:
            try:
                if meta.form_type == 'file':
                    if not request.POST[meta.slug]:
                        continue
                    val = db.Blob(request.POST[meta.slug])
                    setattr(item, meta.slug, val)
                else:
                    setattr(item, meta.slug, request.POST[meta.slug])
            except: pass
    item.put()
    return item

def save_training(request, pid=None, status=None):
    if status == 'edit':
        item = db.get(pid)
        if not item:
            return
        item.group = item.group.key()
    else:
        item = GroupTraining()
        item1 = db.get(pid)
        item.group = item1.key()
    if request.POST['manajemen_usaha']:
        item.manajemen_usaha = int(request.POST['manajemen_usaha'])
    if request.POST['pembukuan']:
        item.pembukuan = int(request.POST['pembukuan'])
    if request.POST['produksi']:
        item.produksi = int(request.POST['produksi'])
    if request.POST['pemanfaatan_limbah']:
        item.pemanfaatan_limbah = int(request.POST['pemanfaatan_limbah'])
    if request.POST['pengemasan']:
        item.pengemasan = int(request.POST['pengemasan'])
    if request.POST['akses_pasar']:
        item.akses_pasar = int(request.POST['akses_pasar'])
    if request.POST['keuangan_mikro']:
        item.keuangan_mikro = int(request.POST['keuangan_mikro'])
    if request.POST['hitung_hpp_harga_jual']:
        item.hitung_hpp_harga_jual = int(request.POST['hitung_hpp_harga_jual'])
    if request.POST['navigasi']:
        item.navigasi = int(request.POST['navigasi'])
    if request.POST['keselamatan_laut']:
        item.keselamatan_laut = int(request.POST['keselamatan_laut'])
    if request.POST['penanganan_atas_kapal']:
        item.penanganan_atas_kapal = int(request.POST['penanganan_atas_kapal'])
    if request.POST['kontrol_kualitas']:
        item.kontrol_kualitas = int(request.POST['kontrol_kualitas'])
    if request.POST['rawat_mesin']:
        item.rawat_mesin = int(request.POST['rawat_mesin'])
    if request.POST['rescue']:
        item.rescue = int(request.POST['rescue'])
    item.put()
    return item

def delete(request, pid):
    item = db.get(pid)
    if item:
        item.delete()
        counter.update('site_group_count', -1)
    return redirect(request, '/group')

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20
    if not Group.objects.all()[:1]:
        Group.counter_reset()
    offset = Group.counter_value()
    sources = LiveGroup.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = GroupContainer.objects.filter(livegroup=str(source.key()))
        if target:
            continue
        try:
            key = source.livecluster.key()
        except db.ReferencePropertyResolveError, e:
            errors.append([source, e])
            continue
        target = Group(name=source.name,
            info=source.info or '',
            geo_pos=source.geo_pos or '',
            livecenter=Container.objects.filter(livecenter=str(source.containers[0]))[0].livelihood)
        c = ClusterContainer.objects.filter(livecluster=str(key))[:1]
        if c:
            target.cluster = c[0].cluster
        photo = FileContainer.objects.filter(container=str(source.key()))[:1]
        if photo:
            target.photo = photo[0].file
        target.save()
        c = GroupContainer(group=target, livegroup=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'group/migrate.html', {
        'targets': targets,
        'errors': errors,
        })


