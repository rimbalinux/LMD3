from django.db import models
from livecenter.models import Livelihood, DistrictModel
from group.models import Group
from counter.tools import BaseModel


class People(DistrictModel): # was livecenter.Person
    GENDERS = (
        (True, 'Male'),
        (False, 'Female'),
        )
    name = models.CharField('nama', max_length=100)
    livecenter = models.ForeignKey(Livelihood)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name='kelompok', related_name='+')
    email = models.EmailField('email', blank=True)
    gender = models.BooleanField('jenis kelamin', choices=GENDERS, default=True)
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

"""
class Container(models.Model): # Tabel peralihan
    people = models.ForeignKey(People)
    person = models.CharField(max_length=100, unique=True) # livecenter.Person.__key__
""" 

class Training(BaseModel): # was livecenter.PersonTraining
    person = models.ForeignKey(People)
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

