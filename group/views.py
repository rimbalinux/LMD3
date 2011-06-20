import urllib
from datetime import date
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from authority.decorators import permission_required_or_403
from livecenter.models import Metaform, Cluster, Livelihood
from livecenter.utils import redirect, default_location
from people.models import People
from product.models import Product
from .models import Group, Report, Training
from .forms import GroupForm, ReportForm, TrainingForm
#from livecenter.models import LiveGroup, LiveCenter, MetaForm, Report_Group, \
#        GroupTraining, LiveCluster, Container, ClusterContainer, Cluster
#from .models import Container as GroupContainer, ReportContainer, TrainingContainer
#from livecenter.utils import migrate_photo
#from google.appengine.ext import db
#import counter


def destination(pid, tabname):
    return '/group/show/%d?tab=%s' % (pid, tabname)
    #return urllib.quote('/group/show/%d?tab=%s' % (pid, tabname))

def index(request):
    limit = 20
    page = 'page' in request.GET and int(request.GET['page']) or 1
    offset = page * limit - limit
    groups = []
    q = Group.objects.all().order_by('-updated')
    for group in q[offset:offset+limit]:
        if group.allowed:
            groups.append(group)
    return direct_to_template(request, 'group/index.html', {
        'groups': groups, 
        'count': Group.counter_value(),
        'lokasi': default_location(),
        'next': q[offset+limit:offset+limit+2] and page+1 or None,
        'prev': q[offset and offset-1 or 0:offset] and page-1,
        })

def show(request, gid):
    group = Group.objects.get(pk=gid)
    other_groups = [] 
    if group.cluster:
        other_groups = Group.objects.filter(cluster=group.cluster).exclude(pk=group.id)
    if not other_groups[:1]:
        other_groups = Group.objects.filter(livecenter=group.livecenter).exclude(pk=group.id)
    trainings = Training.objects.filter(group=group)[:1]
    training = trainings and trainings[0] or None
    return direct_to_template(request, 'group/show.html', {
        'group': group,
        'members': People.objects.filter(group=group),
        'other_groups': other_groups,
        'customfields': Metaform.objects.filter(meta_type='group').\
                filter(category__in=group.livecenter.category),
        'reports': Report.objects.filter(group=group),
        'training': training, 
        'lokasi': group.geo_pos or default_location(),
        })
 
def create(request, lid):
    lc = Livelihood.objects.get(pk=lid)
    group = Group(livecenter=lc)
    return show_edit(request, group)

def edit(request, gid):
    group = Group.objects.get(pk=gid)
    return show_edit(request, group)

@permission_required_or_403('group.change_group')
def show_edit(request, group):
    form = GroupForm(instance=group)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request, '/group/show/%d' % group.id)
    return direct_to_template(request, 'group/edit.html', {
        'form': form,
        'customfields': Metaform.objects.filter(meta_type='group').\
                filter(category__in=group.livecenter.category),
        })

@permission_required_or_403('group.change_group')
def delete(request, gid):
    group = Group.objects.get(pk=gid)
    if request.POST:
        if 'delete' in request.POST:
            _delete(group)
            return redirect(request, '/group')
        return redirect(request, '/group/show/%d' % group.id)
    return direct_to_template(request, 'group/delete.html', {
        'instance': group,
        })

def _delete(group):
    for member in People.objects.filter(group=group):
        for product in Product.objects.filter(person=member):
            product.delete()
        member.delete()
    group.delete()

def report_create(request, gid):
    group = Group.objects.get(pk=gid)
    report = Report(group=group, livecenter=group.livecenter)
    return report_show(request, report)

def report_edit(request, rid):
    report = Report.objects.get(pk=rid)
    return report_show(request, report)

def report_show(request, report):
    form = ReportForm(instance=report)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request, destination(report.group.id, 'laporan'))
    return direct_to_template(request, 'group/report/edit.html', {
        'form': form,
        })

def report_delete(request, rid):
    report = Report.objects.get(pk=rid)
    if request.POST:
        if 'delete' in request.POST:
            report.delete()
        return redirect(request, destination(report.group.id, 'laporan'))
    return direct_to_template(request, 'group/report/delete.html', {
        'instance': report,
        })

def training_create(request, gid):
    group = Group.objects.get(pk=gid)
    training = Training(group=group)
    return training_show_edit(request, training)

def training_edit(request, tid):
    training = Training.objects.get(pk=tid)
    return training_show_edit(request, training)

def training_show_edit(request, training):
    form = TrainingForm(instance=training)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(request, destination(training.group.id, 'pelatihan'))
    return direct_to_template(request, 'group/training/edit.html', {
        'form': form,
        })

def training_delete(request, tid):
    training = Training.objects.get(pk=tid)
    if request.POST:
        if 'delete' in request.POST:
            training.delete()
        return redirect(request, destination(training.group.id, 'pelatihan'))
    return direct_to_template(request, 'group/training/delete.html', {
        'instance': training,
        })



"""
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
"""


# Hitung ulang jumlah group pada suatu livecenter. Sebelum fungsi ini
# dipanggil, pastikan seluruh field group_count = 0 pada tabel
# livecenter_livelihood.
"""
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
"""

##################
# Migrate Report #
##################
# s = 05-MAY-2010
"""
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
"""

####################
# Migrate Training #
####################
"""
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

def migrate_member_count(request):
    counter_name = '__group_member_count_is_not_null_offset'
    offset = counter.get(counter_name)
    targets = []
    for group in Group.objects.order_by('id')[offset:offset+20]:
        if not group.member_count:
            group.member_count = 0
            group.save()
        counter.increment(counter_name)
        targets.append(group)
    return direct_to_template(request, 'group/migrate_member_count.html', {
        'targets': targets,
        })

"""
