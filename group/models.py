from django.db import models
from livecenter.models import Livelihood, Cluster
from counter.tools import BaseModel
from livecenter.tools import GeoModel


class Group(GeoModel): # was LiveGroup
    name = models.CharField('nama kelompok', max_length=100)
    info = models.TextField('keterangan', blank=True)
    cluster = models.ForeignKey(Cluster)
    livecenter = models.ForeignKey(Livelihood)
    member_count = models.IntegerField(default=0,null=True,blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def before_save(self, *args, **kwargs):
        super(Group, self).before_save(*args, **kwargs)
        self.livecenter = self.cluster.livecenter

    def after_save(self, *args, **kwargs):
        super(Group, self).after_save(*args, **kwargs)
        if self.is_insert:
            self.livecenter_counter()

    def delete(self, *args, **kwargs):
        super(Group, self).delete(*args, **kwargs)
        self.livecenter_counter(-1)

    def livecenter_counter(self, add=1):
        self.livecenter.group_count += add 
        self.livecenter.save()



class Container(models.Model): # temporary migration
    group = models.ForeignKey(Group)
    livegroup = models.CharField(max_length=100, unique=True) # references LiveGroup.__key__


class Training(BaseModel): # was livecenter.GroupTraining
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

class TrainingContainer(models.Model):
    new = models.ForeignKey(Training)
    old = models.CharField(max_length=100)

class Report(BaseModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group)
    cluster = models.ForeignKey(Cluster)
    livecenter = models.ForeignKey(Livelihood) 
    date = models.DateField()
    info = models.TextField()

    def before_save(self, *args, **kwargs):
        super(Report, self).before_save(*args, **kwargs)
        self.cluster = self.group.cluster
        self.livecenter = self.cluster.livecenter


class ReportContainer(models.Model):
    new = models.ForeignKey(Report)
    old = models.CharField(max_length=100)
