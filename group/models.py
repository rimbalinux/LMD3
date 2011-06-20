import datetime
from django.db import models
from livecenter.models import Livelihood, Cluster
from counter.tools import BaseModel
from livecenter.tools import GeoModel
from translate.lang import tr


class Group(GeoModel): # was LiveGroup
    name = models.CharField('nama kelompok', max_length=100)
    info = models.TextField('keterangan', blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True, verbose_name='gugusan')
    livecenter = models.ForeignKey(Livelihood)
    member_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def before_save(self, *args, **kwargs):
        super(Group, self).before_save(*args, **kwargs)
        if self.cluster:
            self.livecenter = self.cluster.livecenter

    def after_save(self, *args, **kwargs):
        super(Group, self).after_save(*args, **kwargs)
        if self.is_insert:
            self.livecenter_counter()

    def before_delete(self):
        super(Group, self).before_delete()
        for training in Training.objects.filter(group=self):
            training.delete()
        for report in Report.objects.filter(group=self):
            report.delete()

    def after_delete(self):
        super(Group, self).after_delete()
        self.livecenter_counter(-1)

    def livecenter_counter(self, add=1):
        self.livecenter.group_count += add 
        self.livecenter.save()

    @property
    def allowed(self):
        return super(Group, self).allowed and self.livecenter.allowed

"""
class Container(models.Model): # temporary migration
    group = models.ForeignKey(Group)
    livegroup = models.CharField(max_length=100, unique=True) # references LiveGroup.__key__
"""

def training_choices():
    kali = tr('kali')
    items = []
    for i in range(20):
        items.append((i,'%d %s' % (i, kali)))
    return items

class Training(BaseModel): # was livecenter.GroupTraining
    group = models.ForeignKey(Group)
    manajemen_usaha = models.IntegerField('manajemen usaha', choices=training_choices(), default=0)
    pembukuan = models.IntegerField('pembukuan', choices=training_choices(), default=0)
    produksi = models.IntegerField('produksi', choices=training_choices(), default=0)
    pemanfaatan_limbah = models.IntegerField('pemanfaatan limbah', choices=training_choices(), default=0)
    pengemasan = models.IntegerField('pengemasan', choices=training_choices(), default=0)
    akses_pasar = models.IntegerField('akses pasar', choices=training_choices(), default=0)
    keuangan_mikro = models.IntegerField('keuangan mikro', choices=training_choices(), default=0)
    hitung_hpp_harga_jual = models.IntegerField('perhitungan harga pokok produksi dan harga jual', choices=training_choices(), default=0)
    navigasi = models.IntegerField('navigasi', choices=training_choices(), default=0)
    keselamatan_laut = models.IntegerField('keselamatan di laut', choices=training_choices(), default=0)
    penanganan_atas_kapal = models.IntegerField('penanganan di atas kapal', choices=training_choices(), default=0)
    kontrol_kualitas = models.IntegerField('kontrol kualitas', choices=training_choices(), default=0)
    rawat_mesin = models.IntegerField('perawatan mesin', choices=training_choices(), default=0)
    rescue = models.IntegerField('penyelamatan', choices=training_choices(), default=0)

"""
class TrainingContainer(models.Model):
    new = models.ForeignKey(Training)
    old = models.CharField(max_length=100)
"""

class Report(BaseModel):
    name = models.CharField('nama laporan', max_length=100)
    group = models.ForeignKey(Group, verbose_name='kelompok')
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    livecenter = models.ForeignKey(Livelihood, verbose_name='mata pencaharian')
    day = models.DateField('periode laporan', default=datetime.date.today())
    info = models.TextField('keterangan')

    def before_save(self, *args, **kwargs):
        super(Report, self).before_save(*args, **kwargs)
        self.cluster = self.group.cluster
        self.livecenter = self.cluster.livecenter


"""
class ReportContainer(models.Model):
    new = models.ForeignKey(Report)
    old = models.CharField(max_length=100)
"""
