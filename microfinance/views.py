from livecenter.models import MicroFinance, LivelihoodLocation, Location
from livecenter.utils import getLocation, default_location, migrate_photo
from attachment.utils import save_file_upload
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter
from .models import Finance, Container


def index(request):
    return direct_to_template(request, 'microfinance/index.html', {
        'finances': Finance.objects.all(),
        'count': Finance.counter_value(),
        'lokasi': default_location(), 
        })

def show(request, pid):
    item = db.get(pid)
    if not item:
        return HttpResponseRedirect('/microfinance')

    kontak = [
        ['Nama', item.contact_name],
        ['Telepon selular', item.mobile],
        ['Alamat', item.address],
        ['Kabupaten', item.district.dl_name],
        ['Kecamatan', item.sub_district.dl_name],
        ]

    keuangan = [
        ['Tipe LKM', item.kind_lkm],
        ['Total aset', '%d Rupiah' % item.total_asset],
        ['Total penyediaan dana pinjaman', '%d Rupiah' % item.total_sedia_dana_pinjaman],
        ['Total pencairan', '%d Rupiah' % item.total_penyaluran],
        ['Sektor usaha', item.sektor_usaha],
        ['Persyaratan pinjaman', item.persyaratan_pinjaman],
        ['Persyaratan agunan', item.persyaratan_agunan],
        ['Jangkauan wilayah usaha', item.jangkauan_wilayah_usaha],
        ['Nilai pinjaman maksimum', item.nilai_maks_pinjaman],
        ['Jangka waktu pinjaman', item.jangka_wkt_pinjaman],
        ['Bunga pinjaman', '%s %%' % item.margin_bunga],
        ['Bantuan untuk penerima manfaat JFPR', item.bantuan_penerima_mamfaat_jfpr],
        ['Pelatihan', '<none>'],
        ['Pengelolaan usaha', '%d kali' % item.manajemen_usaha],
        ['Pembukuan', '%d kali' % item.pembukuan],
        ['Akses pasar', '%d kali' % item.akses_pasar],
        ['Keuangan mikro', '%d kali' % item.keuangan_mikro],
        ['Penguatan pelayanan', '<none>'],
        ['Petugas akun', '%d kali' % item.ao],
        ['Layanan pelanggan', '%d kali' % item.cs],
        ['Kasir', '%d kali' % item.tl],
        ['Kelayakan usaha', '%d kali' % item.kelayakan_usaha],
        ]

    return direct_to_template(request, 'microfinance/show.html', {
        'microfinance': item,
        'kontak': kontak,
        'keuangan': keuangan,
        'lokasi': default_location(),
        })

def create(request):
    if request.POST: 
        micro = save(request)
        return HttpResponseRedirect('/microfinance/show/%s' % micro.key())
    return direct_to_template(request, 'microfinance/create.html', {
        'pagetitle': 'Tambah Keuangan Mikro',
        'district_sel': 0,
        'subdistrict_sel': 0,
        'village_sel': 0,
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        })

def edit(request, pid):
    if request.POST:
        micro = save(request, pid)
        if micro:
            return HttpResponseRedirect('/microfinance/show/%s' % micro.key())
        return HttpResponseRedirect('/microfinance')
    micro = db.get(pid)
    return direct_to_template(request, 'microfinance/edit.html', {
        'pagetitle': 'Ubah ' + micro.name_org,
        'micro': micro,
        'geo_pos': micro.geo_pos,
        'districts': LivelihoodLocation().all().filter('dl_parent = ',0),
        'district_sel': micro.district.dl_id,
        'subdistrict_sel': micro.sub_district.dl_id,
        })

def save(request, pid=None):
    if pid:
        micro = db.get(pid)
        if not micro:
            return
    else:
        micro = MicroFinance()
    micro.name_org = request.POST['name_org']
    micro.contact_name = request.POST['contact_name']
    micro.geo_pos = request.POST['geo_pos'] or default_location() 
    micro.district = getLocation(request.POST['district']).key()
    micro.sub_district = getLocation(request.POST['sub_district']).key()
    micro.kind_lkm = request.POST['kind_lkm']
    if request.POST['total_asset']:
        micro.total_asset = int(request.POST['total_asset'])
    if request.POST['total_sedia_dana_pinjaman']:
        micro.total_sedia_dana_pinjaman  = int(request.POST['total_sedia_dana_pinjaman'])
    if request.POST['total_penyaluran']:
        micro.penyaluran  = int(request.POST['total_penyaluran'])
    micro.sektor_usaha = request.POST['sektor_usaha']
    micro.persyaratan_pinjaman = request.POST['persyaratan_pinjaman']
    micro.persyaratan_agunan = request.POST['persyaratan_agunan']
    micro.jangkauan_wilayah_usaha = request.POST['jangkauan_wilayah_usaha']
    micro.nilai_maks_pinjaman = request.POST['nilai_maks_pinjaman']
    micro.jangka_wkt_pinjaman = request.POST['jangka_wkt_pinjaman']
    micro.margin_bunga = request.POST['margin_bunga']
    micro.bantuan_penerima_mamfaat_jfpr = request.POST['bantuan_penerima_mamfaat_jfpr']
    if request.POST['manajemen_usaha']:
        micro.manajemen_usaha  = int(request.POST['manajemen_usaha'])
    if request.POST['pembukuan']:
        micro.pembukuan  = int(request.POST['pembukuan'])
    if request.POST['akses_pasar']:
        micro.akses_pasar  = int(request.POST['akses_pasar'])
    if request.POST['keuangan_mikro']:
        micro.keuangan_mikro  = int(request.POST['keuangan_mikro'])
    if request.POST['ao']:
        micro.ao  = int(request.POST['ao'])
    if request.POST['cs']:
        micro.cs  = int(request.POST['cs'])
    if request.POST['tl']:
        micro.tl  = int(request.POST['tl'])
    if request.POST['kelayakan_usaha']:
        micro.kelayakan_usaha  = int(request.POST['kelayakan_usaha'])
    if request.POST['address']:
        micro.address  = request.POST['address']
    if request.POST['mobile']:
        micro.mobile   = request.POST['mobile']
    micro.put()
    if not pid:
        counter.update('site_micro_count', 1)
    save_file_upload(request, 'photo', micro)
    return micro

def delete(request, pid=None):
    if not pid:
        return HttpResponseRedirect('/microfinance')
    item = db.get( pid )
    if not item:
        return HttpResponseRedirect('/microfinance')
    counter.update('site_micro_count', -1)
    item.delete()
    return HttpResponseRedirect('/microfinance')

def migrate(request):
    limit = 'limit' in request.GET and int(request.GET['limit']) or 20 
    offset = len(Finance.objects.all())
    sources = MicroFinance.all().order('__key__')
    targets = []
    for source in sources.fetch(limit=limit, offset=offset):
        target = Container.objects.filter(microfinance=str(source.key()))
        if target:
            continue
        target = Finance(
            name_org=source.name_org,
            contact_name=source.contact_name,
            address=source.address,
            geo_pos=str(source.geo_pos) != 'nan,nan' and source.geo_pos or '',
            sub_district=source.sub_district and Location.objects.filter(lid=source.sub_district.dl_id)[0] or None,
            district=source.district and Location.objects.filter(lid=source.district.dl_id)[0] or None,
            mobile=source.mobile,
            kind_lkm=source.kind_lkm,
            total_asset=source.total_asset,
            total_sedia_dana_pinjaman=source.total_sedia_dana_pinjaman,
            total_penyaluran=source.total_penyaluran,
            sektor_usaha=source.sektor_usaha,
            persyaratan_pinjaman=source.persyaratan_pinjaman,
            persyaratan_agunan=source.persyaratan_agunan,
            jangkauan_wilayah_usaha=source.jangkauan_wilayah_usaha,
            nilai_maks_pinjaman=source.nilai_maks_pinjaman,
            jangka_wkt_pinjaman=source.jangka_wkt_pinjaman,
            margin_bunga=source.margin_bunga,
            bantuan_penerima_manfaat_jfpr=source.bantuan_penerima_mamfaat_jfpr,
            manajemen_usaha=source.manajemen_usaha,
            pembukuan=source.pembukuan,
            akses_pasar=source.akses_pasar,
            keuangan_mikro=source.keuangan_mikro,
            ao=source.ao,
            cs=source.cs,
            tl=source.tl,
            kelayakan_usaha=source.kelayakan_usaha,
            photo=migrate_photo(request, source))
        target.save()
        c = Container(finance=target, microfinance=str(source.key()))
        c.save()
        targets.append(target)
    return direct_to_template(request, 'microfinance/migrate.html', {
        'targets': targets, 
        })

def migrate_delete(request): # danger
    limit = 20
    targets = []
    for target in Finance.objects.all()[:limit]:
        targets.append(target)
        target.delete()
    for c in Container.objects.all()[:limit]:
        c.delete()
    return direct_to_template(request, 'microfinance/migrate.html', {
        'targets': targets, 
        })

