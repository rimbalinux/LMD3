from google.appengine.ext import db
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from livecenter.utils import default_location, redirect
import counter
from .models import Finance
from .forms import FinanceForm
#from livecenter.models import MicroFinance, LivelihoodLocation, Location
#from livecenter.utils import migrate_photo
#from .models import Container


def index(request):
    return direct_to_template(request, 'microfinance/index.html', {
        'finances': Finance.objects.all(),
        'count': Finance.counter_value(),
        'lokasi': default_location(), 
        })

def show(request, mid):
    mf = Finance.objects.get(pk=mid)

    kontak = [
        ['Nama', mf.contact_name],
        ['Telepon selular', mf.mobile],
        ['Alamat', mf.address],
        ['Kabupaten', mf.district.name],
        ['Kecamatan', mf.sub_district.name],
        ]

    keuangan = [
        ['Tipe LKM', mf.kind_lkm],
        ['Total aset', '%d Rupiah' % mf.total_asset],
        ['Total penyediaan dana pinjaman', '%d Rupiah' % mf.total_sedia_dana_pinjaman],
        ['Total pencairan', '%d Rupiah' % mf.total_penyaluran],
        ['Sektor usaha', mf.sektor_usaha],
        ['Persyaratan pinjaman', mf.persyaratan_pinjaman],
        ['Persyaratan agunan', mf.persyaratan_agunan],
        ['Jangkauan wilayah usaha', mf.jangkauan_wilayah_usaha],
        ['Nilai pinjaman maksimum', mf.nilai_maks_pinjaman],
        ['Jangka waktu pinjaman', mf.jangka_wkt_pinjaman],
        ['Bunga pinjaman', '%s %%' % mf.margin_bunga],
        ['Bantuan untuk penerima manfaat JFPR', mf.bantuan_penerima_manfaat_jfpr],
        ['Pelatihan', '<none>'],
        ['Pengelolaan usaha', '%d kali' % mf.manajemen_usaha],
        ['Pembukuan', '%d kali' % mf.pembukuan],
        ['Akses pasar', '%d kali' % mf.akses_pasar],
        ['Keuangan mikro', '%d kali' % mf.keuangan_mikro],
        ['Penguatan pelayanan', '<none>'],
        ['Petugas akun', '%d kali' % mf.ao],
        ['Layanan pelanggan', '%d kali' % mf.cs],
        ['Kasir', '%d kali' % mf.tl],
        ['Kelayakan usaha', '%d kali' % mf.kelayakan_usaha],
        ]

    return direct_to_template(request, 'microfinance/show.html', {
        'microfinance': mf,
        'kontak': kontak,
        'keuangan': keuangan,
        'lokasi': default_location(mf.geo_pos),
        })

def create(request):
    mf = Finance()
    return show_edit(request, mf)

def edit(request, mid):
    mf = Finance.objects.get(pk=mid)
    return show_edit(request, mf)

def show_edit(request, mf):
    if request.POST:
        form = FinanceForm(instance=mf.id and mf or None)
        if form.is_valid():
            form.save()
            return redirect(request, '/microfinance/show/%d' % mf.id)
    else:
        form = FinanceForm(instance=mf)
    return direct_to_template(request, 'microfinance/edit.html', {
        'form': form
        })

def delete(request, mid):
    mf = Finance.objects.get(pk=mid)
    mf.delete()
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

