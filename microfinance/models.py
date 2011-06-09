from django.db import models
from livecenter.models import Location
from livecenter.tools import GeoModel
from translate.lang import tr

KATA_TIPE = tr('Tipe')

TIPE_PINJAMAN = (
    ('Type A', '%s %s' % (KATA_TIPE, 'A')),
    ('Type B', '%s %s' % (KATA_TIPE, 'B')),
    ('Type C', '%s %s' % (KATA_TIPE, 'C'))
    )

SYARAT_AGUNAN = (
    ('Ya', tr('Ya')),
    ('Tidak', tr('Tidak'))
    )
 
JFPR = (
    ('Ada', tr('Ada')),
    ('Belum', tr('Belum'))
    )


class Finance(GeoModel):
    name_org  = models.CharField('nama organisasi', max_length=100) 
    contact_name = models.CharField('nama kontak', max_length=100) 
    address = models.CharField('alamat', max_length=100) 
    sub_district = models.ForeignKey(Location, null=True, related_name='+', verbose_name='kecamatan') 
    district = models.ForeignKey(Location, null=True, related_name='+', verbose_name='kabupaten') 
    mobile = models.CharField('telepon selular', max_length=20, blank=True) 
    kind_lkm = models.CharField('jenis lembaga keuangan mikro', max_length=100, blank=True) 
    total_asset = models.IntegerField('total aset', default=0, help_text='IDR')
    total_sedia_dana_pinjaman = models.IntegerField('total penyediaan dana pinjaman', default=0) 
    total_penyaluran = models.IntegerField('total penyaluran', default=0, help_text='IDR') 
    sektor_usaha = models.CharField('sektor usaha yang dibiayai', max_length=100, blank=True) 
    persyaratan_pinjaman = models.CharField('persyaratan peminjaman', max_length=100, choices=TIPE_PINJAMAN)
    persyaratan_agunan = models.CharField('persyaratan agunan', max_length=100, choices=SYARAT_AGUNAN) 
    jangkauan_wilayah_usaha = models.CharField('jangkauan wilayah usaha', max_length=100, blank=True) 
    nilai_maks_pinjaman = models.CharField('nilai maksimal pinjaman', max_length=100) 
    jangka_wkt_pinjaman = models.CharField('jangka waktu pinjaman', max_length=100, blank=True) 
    margin_bunga = models.CharField('bunga pinjaman', max_length=100) 
    bantuan_penerima_manfaat_jfpr = models.CharField('bantuan untuk penerima manfaat JFPR', max_length=100, choices=JFPR) 
    manajemen_usaha = models.IntegerField('manajemen usaha', default=0)
    pembukuan = models.IntegerField('pembukuan', default=0) 
    akses_pasar = models.IntegerField('akses pasar', default=0) 
    keuangan_mikro = models.IntegerField('keuangan mikro', default=0) 
    ao = models.IntegerField('petugas akun', default=0) 
    cs = models.IntegerField('layanan pelanggan', default=0) 
    tl = models.IntegerField('kasir', default=0) 
    kelayakan_usaha = models.IntegerField('kelayakan usaha', default=0) 

class Container(models.Model): # Tabel peralihan
    finance = models.ForeignKey(Finance)
    microfinance = models.CharField(max_length=100, unique=True) # livecenter.MicroFinance.__key__
 
