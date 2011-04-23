from livecenter.models import MicroFinance 
from livecenter.views import DEFAULT_LOCATION
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from google.appengine.ext import db
from tipfy.pager import PagerQuery, SearchablePagerQuery
import counter


def index(request):
    q = 'q' in request.GET and request.GET['q']
    page = 'page' in request.GET and request.GET['page']
    prev, items, next = SearchablePagerQuery(MicroFinance).search(q).fetch(12, page)
    return direct_to_template(request, 'microfinance/index.html', {
        'items': items,
        'items_count': counter.get('site_micro_count'),
        'prev': prev,
        'next': next,
        'lokasi': ', '.join(map(lambda x: str(x), DEFAULT_LOCATION)),
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
        ['Bunga pinjaman', '%.2f %%' % item.margin_bunga],
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
        'lokasi': ', '.join(map(lambda x: str(x), DEFAULT_LOCATION)),
        })
