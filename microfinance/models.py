from django.db import models
from livecenter.models import Location
from livecenter.tools import GeoModel


class Finance(GeoModel):
    name_org  = models.CharField(max_length=100) 
    contact_name = models.CharField(max_length=100) 
    address = models.CharField(max_length=100) 
    sub_district = models.ForeignKey(Location, null=True, related_name='+') 
    district = models.ForeignKey(Location, null=True, related_name='+') 
    mobile = models.CharField(max_length=20) 
    kind_lkm = models.CharField(max_length=100) 
    total_asset = models.IntegerField(default=0)
    total_sedia_dana_pinjaman = models.IntegerField(default=0) 
    total_penyaluran = models.IntegerField(default=0) 
    sektor_usaha = models.CharField(max_length=100) 
    persyaratan_pinjaman  = models.CharField(max_length=100) 
    persyaratan_agunan  = models.CharField(max_length=100) 
    jangkauan_wilayah_usaha  = models.CharField(max_length=100) 
    nilai_maks_pinjaman  = models.CharField(max_length=100) 
    jangka_wkt_pinjaman  = models.CharField(max_length=100) 
    margin_bunga  = models.CharField(max_length=100) 
    bantuan_penerima_manfaat_jfpr = models.CharField(max_length=100) 
    manajemen_usaha = models.IntegerField(default=0) 
    pembukuan = models.IntegerField(default=0) 
    akses_pasar = models.IntegerField(default=0) 
    keuangan_mikro = models.IntegerField(default=0) 
    ao = models.IntegerField(default=0) 
    cs = models.IntegerField(default=0) 
    tl = models.IntegerField(default=0) 
    kelayakan_usaha = models.IntegerField(default=0) 

class Container(models.Model): # Tabel peralihan
    finance = models.ForeignKey(Finance)
    microfinance = models.CharField(max_length=100, unique=True) # livecenter.MicroFinance.__key__
 
