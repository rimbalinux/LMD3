from django.db import models
from livecenter.models import Livelihood, Cluster
from counter.tools import BaseModel
from attachment.models import File


class Group(BaseModel):
    name = models.CharField(max_length=100)
    info = models.TextField()
    cluster = models.ForeignKey(Cluster)
    livecenter = models.ForeignKey(Livelihood)
    geo_pos = models.CharField(max_length=100)
    photo = models.ForeignKey(File, null=True)

class Container(models.Model): # temporary migration
    group = models.ForeignKey(Group)
    livegroup = models.CharField(max_length=100, unique=True) # references LiveGroup.__key__


class Training(models.Model): # was livecenter.GroupTraining
    group = models.ForeignKey(Group)
    manajemen_usaha = models.IntegerField()
    pembukuan = models.IntegerField()
    produksi = models.IntegerField()
    pemanfaatan_limbah = models.IntegerField()
    pengemasan = models.IntegerField()
    akses_pasar = models.IntegerField()
    keuangan_mikro = models.IntegerField()
    hitung_hpp_harga_jual = models.IntegerField()
    navigasi = models.IntegerField()
    keselamatan_laut = models.IntegerField()
    penanganan_atas_kapal = models.IntegerField()
    kontrol_kualitas = models.IntegerField()
    rawat_mesin = models.IntegerField()
    rescue = models.IntegerField()


