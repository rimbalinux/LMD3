from django.db import models
from livecenter.models import Location, Livelihood
from group.models import Group
from attachment.models import File
from counter.tools import BaseModel


class People(BaseModel): # was livecenter.Person
    GENDERS = (
        (True, 'Male'),
        (False, 'Female'),
        )
    name = models.CharField(max_length=100)
    livecenter = models.ForeignKey(Livelihood)
    group = models.ForeignKey(Group, null=True)
    email = models.EmailField()
    gender = models.BooleanField(choices=GENDERS)
    birth_year = models.IntegerField(null=True)
    birth_place = models.CharField(max_length=100)
    address = models.TextField()
    village = models.ForeignKey(Location, related_name='+')
    sub_district = models.ForeignKey(Location, related_name='+')
    district = models.ForeignKey(Location, related_name='+')
    education = models.CharField(max_length=100)
    spouse_name = models.CharField(max_length=100)
    monthly_income = models.IntegerField(null=True)
    children_num = models.IntegerField(null=True)
    member_type = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    info = models.TextField()
    geo_pos = models.CharField(max_length=100)
    photo = models.ForeignKey(File, null=True)
    updated = models.DateTimeField(auto_now=True)

class Container(models.Model): # Tabel peralihan
    people = models.ForeignKey(People)
    person = models.CharField(max_length=100, unique=True) # livecenter.Person.__key__
    

class Training(models.Model): # was livecenter.PersonTraining
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


