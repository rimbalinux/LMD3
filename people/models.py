from django.db import models
from livecenter.models import Livelihood, DistrictModel
from group.models import Group, training_choices
from counter.tools import BaseModel
from translate.lang import tr

def genders():
    return (
        (True, tr('Laki-laki')),
        (False, tr('Perempuan')),
        )


class People(DistrictModel): # was livecenter.Person
    name = models.CharField('nama', max_length=100)
    livecenter = models.ForeignKey(Livelihood)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name='kelompok', related_name='+')
    email = models.EmailField('email', blank=True)
    gender = models.BooleanField('jenis kelamin', choices=genders(), default=True)
    birth_year = models.IntegerField('tahun lahir', null=True, blank=True)
    birth_place = models.CharField('tempat lahir', max_length=100, blank=True)
    address = models.TextField('alamat', blank=True)
    education = models.CharField('pendidikan', max_length=100, blank=True)
    spouse_name = models.CharField('nama pasangan', max_length=100, blank=True)
    monthly_income = models.IntegerField('pendapatan bulanan', null=True, blank=True)
    children_num = models.IntegerField('jumlah tanggungan', null=True, blank=True)
    member_type = models.CharField('jenis anggota', max_length=100, blank=True)
    mobile = models.CharField('telepon selular', max_length=20, blank=True)
    info = models.TextField('catatan', blank=True)

    def before_save(self, *args, **kwargs):
        super(People, self).before_save(*args, **kwargs)
        if self.group:
            self.livecenter = self.group.livecenter

    def after_save(self, *args, **kwargs):
        super(People, self).after_save(*args, **kwargs)
        if self.is_insert:
            self.livecenter_counter()
            self.member_counter()

    def delete(self, *args, **kwargs):
        super(People, self).delete(*args, **kwargs)
        self.livecenter_counter(-1)
        self.member_counter(-1)

    def livecenter_counter(self, add=1):
        self.livecenter.member_count += add 
        self.livecenter.save()

    def member_counter(self, add=1):
        if not self.group:
            return
        self.group.member_count += 1
        self.group.save()

    @property
    def allowed(self):
        return super(People, self).allowed and self.livecenter.allowed

"""
class Container(models.Model): # Tabel peralihan
    people = models.ForeignKey(People)
    person = models.CharField(max_length=100, unique=True) # livecenter.Person.__key__
""" 

class Training(BaseModel): # was livecenter.PersonTraining
    person = models.ForeignKey(People, verbose_name='nama anggota')
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

