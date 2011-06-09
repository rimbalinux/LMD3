import urllib
from datetime import date
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from livecenter.models import Metaform
from livecenter.utils import redirect, default_location, migrate_photo
from people.models import People
from .models import Group, Report, Training
from .forms import GroupForm
#from livecenter.models import LiveGroup, LiveCenter, MetaForm, Report_Group, \
#        GroupTraining, LiveCluster, Container, ClusterContainer, Cluster
#from .models import Container as GroupContainer, ReportContainer, TrainingContainer


def destination(pid, tabname):
    return urllib.quote('/group/show/%s?tab=%s' % (pid, tabname))

def index(request):
    return direct_to_template(request, 'group/index.html', {
        'groups': Group.objects.all(), 
        'count': Group.counter_value(),
        'lokasi': default_location(), 
        })

def show(request, gid):
    group = Group.objects.get(pk=gid)
    return direct_to_template(request, 'group/show.html', {
        'group': group,
        'members': People.objects.filter(group=group),
        'other_groups': Group.objects.filter(cluster=group.cluster).exclude(pk=group.id),
        'customfields': Metaform.objects.filter(meta_type='group').\
                filter(category__in=group.livecenter.category),
        'reports': Report.objects.filter(group=group),
        'trainings': Training.objects.filter(group=group),
        'lokasi': group.geo_pos or default_location(),
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
 
def create(request, cid):
    cluster = Cluster.objects.get(pk=cid)
    group = Group(cluster=cluster, livecenter=cluster.livecenter)
    return show_edit(request, group)

def edit(request, gid):
    group = Group.objects.get(pk=gid)
    return show_edit(request, group)

def show_edit(request, group):
    if request.POST:
        form = GroupForm(instance=group.id and group or None)
        if form.is_valid():
            form.save()
            return redirect(request)
    else:
        form = GroupForm(instance=group)
    return direct_to_template(request, 'group/edit.html', {
        'form': form,
        'customfields': Metaform.objects.filter(meta_type='group').\
                filter(category__in=group.livecenter.category),
        })

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
    #if not Group.objects.all()[:1]:
    #    Group.counter_reset()
    offset = Group.counter_value()
    sources = LiveGroup.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = GroupContainer.objects.filter(livegroup=str(source.key()))
        if target:
            continue
        try:
            cluster_key = source.livecluster.key()
        except db.ReferencePropertyResolveError, e:
            errors.append([source, e])
            continue
        livecenter_key = str(source.containers[0])
        c = Container.objects.get(livecenter=livecenter_key)
        if c:
            livecenter = c.livelihood
        else:
            errors.append([source, 'Livecenter %s tidak ada' % livecenter_key])
            continue
        target = Group(name=source.name,
            info=source.info or '',
            geo_pos=str(source.geo_pos) != 'nan,nan' and source.geo_pos or '',
            livecenter=livecenter)
        c = ClusterContainer.objects.filter(livecluster=str(cluster_key))[:1]
        if c:
            target.cluster = c[0].cluster
        target.photo = migrate_photo(request, source)
        target.save()
        c = GroupContainer(group=target, livegroup=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'group/migrate.html', {
        'targets': targets,
        'errors': errors,
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Group.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in GroupContainer.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'group/migrate.html', {
        'targets': targets,
        })


# Hitung ulang jumlah group pada suatu livecenter. Sebelum fungsi ini
# dipanggil, pastikan seluruh field group_count = 0 pada tabel
# livecenter_livelihood.
def livecenter_group_count(request):
    counter_name = '__livecenter_group_count_offset'
    offset = counter.get(counter_name)
    targets = []
    for g in Group.objects.order_by('id')[offset:20]:
        g.livecenter.group_count += 1
        g.livecenter.save()
        counter.increment(counter_name)
        targets.append(g)
    return direct_to_template(request, 'group/livecenter_group_count.html', {
        'targets': targets,
        })

##################
# Migrate Report #
##################
# s = 05-MAY-2010
def migrate_date(s):
    months = ['','JAN','FEB','MAR','APR','MAY','JUN','JUL','AGT','SEP','OKT','NOP','DES']
    t = s.split('-')
    return date(int(t[2]), months.index(t[1]), int(t[0])) 

  
def migrate_report(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20
    offset = Report.counter_value()
    sources = Report_Group.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = ReportContainer.objects.filter(old=str(source.key()))
        if target:
            continue
        try:
            group_key = source.name_group.key()
        except db.ReferencePropertyResolveError, e:
            errors.append(e)
            continue
        group = GroupContainer.objects.get(livegroup=group_key)
        target = Report(name=source.name,
            group=group.group,
            date=migrate_date(source.year),
            info=source.info or '')
        target.save()
        c = ReportContainer(new=target, old=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'group/migrate_report.html', {
        'targets': targets,
        'errors': errors,
        })

def migrate_report_delete(request): # danger
    limit = 20
    targets = []
    for target in Report.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in ReportContainer.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'group/migrate_report.html', {
        'targets': targets,
        })

####################
# Migrate Training #
####################
def migrate_training(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20
    offset = Training.counter_value()
    sources = GroupTraining.all().order('__key__')
    targets = []
    errors = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = TrainingContainer.objects.filter(old=str(source.key()))
        if target:
            continue
        try:
            group_key = source.group.key()
        except db.ReferencePropertyResolveError, e:
            errors.append(e)
            continue
        group = GroupContainer.objects.get(livegroup=group_key)
        target = Training(
            group=group.group,
            manajemen_usaha=source.manajemen_usaha,
            pembukuan=source.pembukuan,
            produksi=source.produksi,
            pemanfaatan_limbah=source.pemanfaatan_limbah,
            pengemasan=source.pengemasan,
            akses_pasar=source.akses_pasar,
            keuangan_mikro=source.keuangan_mikro,
            hitung_hpp_harga_jual=source.hitung_hpp_harga_jual,
            navigasi=source.navigasi,
            keselamatan_laut=source.keselamatan_laut,
            penanganan_atas_kapal=source.penanganan_atas_kapal,
            kontrol_kualitas=source.kontrol_kualitas,
            rawat_mesin=source.rawat_mesin,
            rescue=source.rescue)
        target.save()
        c = TrainingContainer(new=target, old=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'group/migrate_training.html', {
        'targets': targets,
        'errors': errors,
        })


