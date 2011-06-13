# Sumber: LMD/models.py

#from google.appengine.ext import db, search
from django.db import models
from djangotoolbox import fields
from attachment.models import Attachment
from attachment.tools import PhotoModel
from counter.tools import BaseModel
from .tools import GeoModel


"""
class LivelihoodLocation(db.Model):
    dl_id = db.IntegerProperty()
    dl_name = db.StringProperty()
    dl_parent = db.IntegerProperty()
"""

class Location(BaseModel):
    lid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    parent = models.IntegerField() # references Location.lid

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class DistrictModel(GeoModel):
    district = models.ForeignKey(Location, related_name='+', null=True)
    sub_district = models.ForeignKey(Location, related_name='+', null=True)
    village = models.ForeignKey(Location, related_name='+', null=True)

    class Meta:
        abstract = True


""" 
class LiveCategory(search.SearchableModel):
    ancestor = db.ListProperty(db.Key, default=[])
    no_ancestor = db.BooleanProperty(default=True)
    name = db.StringProperty()
    description = db.TextProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    
    @property
    def enterprises(self):
        return LiveCategory.all().filter("ancestor", self.key())

    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())
    @property
    def parent_cat(self):
        return LiveCategory.gql("WHERE __key__ IN :1", self.ancestor)

    @property
    def metaforms(self):
        return MetaForm.gql("WHERE containers = :1", self.key())
"""


class Category(PhotoModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ancestor = models.ForeignKey('Category', null=True)

    def __unicode__(self):
        return self.name

"""
class CategoryContainer(models.Model): # migrasi
    category = models.ForeignKey(Category)
    livecategory = models.CharField(max_length=100) # references LiveCategory.__key__ 
"""
 
"""
class LiveCenter(search.SearchableModel):
    category = db.ListProperty(db.Key,default=[])
    name = db.StringProperty()
    address = db.TextProperty()
    district = db.ReferenceProperty(LivelihoodLocation, collection_name="district")
    sub_district = db.ReferenceProperty(LivelihoodLocation, collection_name="sub_district")
    village = db.ReferenceProperty(LivelihoodLocation, collection_name="village")
    description = db.TextProperty()
    geo_pos = db.GeoPtProperty()
    last_modified = db.DateTimeProperty(auto_now=True)

    @property
    def categories(self):
        return LiveCategory.gql("WHERE __key__ IN :1", self.category)

    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())

    @property
    def productFields(self):
        return MetaForm.gql("WHERE livecenter = :1 AND meta_type = :2", self.key(), 'product')

    @property
    def groupFields(self):
        return MetaForm.gql("WHERE livecenter = :1 AND meta_type = :2", self.key(), 'group')
    
    @property
    def clusters(self):
        return LiveCluster.gql("WHERE livecenter = :1", self.key())

    @property
    def groups(self):
        return LiveGroup.gql("WHERE containers = :1", self.key())
"""


class Livelihood(DistrictModel): # was LiveCenter
    name = models.CharField(max_length=100)
    category = fields.ListField(verbose_name='kategori', null=True)
    address = models.TextField('alamat')
    description = models.TextField('keterangan')
    member_count = models.IntegerField(default=0, blank=True)
    cluster_count = models.IntegerField(default=0, blank=True)
    group_count = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def categories(self):
        cs = []
        for c in self.category:
            cs.append(Category.objects.get(pk=c))
        return cs


class Container(models.Model): # peralihan, temporary
    livelihood = models.ForeignKey(Livelihood)
    livecenter = models.CharField(max_length=100) # references LiveCenter.__key__ 


"""
class Person(search.SearchableModel):
    livecenter = db.ReferenceProperty(LiveCenter, collection_name='peoples')
    livegroup = db.ListProperty(db.Key,default=[])
    email = db.EmailProperty()
    name = db.TextProperty()
    gender = db.StringProperty()
    birth_year = db.IntegerProperty()
    birth_place = db.StringProperty()
    address = db.PostalAddressProperty()
    village = db.ReferenceProperty(LivelihoodLocation, collection_name="villages")
    sub_district = db.ReferenceProperty(LivelihoodLocation, collection_name="sub_districts")
    district = db.ReferenceProperty(LivelihoodLocation, collection_name="districts")
    education = db.StringProperty()
    spouse_name = db.StringProperty()
    monthly_income = db.IntegerProperty()
    children_num = db.IntegerProperty()
    member_type = db.StringProperty()
    mobile = db.PhoneNumberProperty()
    info = db.TextProperty()
    geo_pos = db.GeoPtProperty()
    last_modified = db.DateTimeProperty(auto_now=True)
    
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())

    @property
    def groups(self):
        if self.livegroup:
            return LiveGroup.gql("WHERE __key__ IN :1", self.livegroup)
    @property
    def clusters(self):
        return LiveCluster.gql("WHERE livecenter = :1", self.livecenter)
""" 

"""
class LiveCluster(search.SearchableModel, db.Expando):
    category = db.ReferenceProperty(LiveCategory, collection_name='clusters')
    livecenter = db.ListProperty(db.Key, default=[])
    name = db.StringProperty()
    info = db.TextProperty()
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())
"""

class Cluster(PhotoModel):
    name = models.CharField('nama gugusan', max_length=100)
    category = models.ForeignKey(Category, verbose_name='kategori')
    livecenter = models.ForeignKey(Livelihood, verbose_name='mata pencaharian')
    info = models.TextField('keterangan', blank=True)

    def __unicode__(self):
        return self.name

    def after_save(self, *args, **kwargs):
        super(Cluster, self).after_save(*args, **kwargs)
        if self.is_insert:
            self.livecenter_counter()

    def delete(self, *args, **kwargs):
        super(Cluster, self).delete(*args, **kwargs)
        self.livecenter_counter(-1)

    def livecenter_counter(self, add=1):
        self.livecenter.cluster_count += add 
        self.livecenter.save()

"""
class ClusterContainer(models.Model): # migrasi, temporary
    cluster = models.ForeignKey(Cluster, unique=True)
    livecluster = models.CharField(max_length=100, unique=True) # references LiveCluster.__key__ 
"""

"""
class LiveGroup(search.SearchableModel, db.Expando):
    livecluster = db.ReferenceProperty(LiveCluster, collection_name='groups')
    containers = db.ListProperty(db.Key,default=[])
    name = db.StringProperty()
    info = db.TextProperty()
    geo_pos = db.GeoPtProperty()
    @property
    def members(self):
        return Person.gql("WHERE livegroup = :1", self.key())
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())

class MetaForm(db.Model):
    meta_type    = db.StringProperty(choices=('product', 'group'), default='product')
    container    = db.ListProperty(db.Key,default=[])
    title        = db.StringProperty()
    slug         = db.StringProperty()
    form_type    = db.StringProperty(choices=('text', 'select', 'photo', 'document', 'textarea', 'geopt'))
    attribute    = db.TextProperty()
    description  = db.TextProperty()
    
    @property
    def categories(self):
        LiveCategory.gql("WHERE __key__ IN :1", self.container)
    
    @property
    def livecenters(self):
        LiveCenter.gql("WHERE __key__ IN :1", self.container)
"""

class Metaform(BaseModel):
    title = models.CharField(max_length=100) 
    meta_type = models.CharField(max_length=100, choices=('product', 'group'),
            default='product')
    category = models.ForeignKey(Category)
    slug = models.CharField(max_length=100)
    form_type = models.CharField(choices=('text', 'select', 'photo', 'document', 'textarea', 'geopt'))
    attribute = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ['title']

"""
class MetaformContainer(models.Model):
    new = models.ForeignKey(Metaform)
    old = models.CharField(max_length=100, unique=True)
"""

"""
Micro Finance
added by Jufri Wahyudi
"""
"""
class MicroFinance(search.SearchableModel):
    name_org  = db.StringProperty()
    contact_name = db.StringProperty()
    address = db.PostalAddressProperty()
    geo_pos = db.GeoPtProperty()
    sub_district = db.ReferenceProperty(LivelihoodLocation, collection_name="sub_districtm")
    district = db.ReferenceProperty(LivelihoodLocation, collection_name="districtm")
    mobile = db.PhoneNumberProperty()
    kind_lkm = db.StringProperty()
    total_asset = db.IntegerProperty(default=0)
    total_sedia_dana_pinjaman = db.IntegerProperty(default=0)
    total_penyaluran = db.IntegerProperty(default=0)
    sektor_usaha  = db.StringProperty()
    persyaratan_pinjaman  = db.StringProperty()
    persyaratan_agunan  = db.StringProperty()
    jangkauan_wilayah_usaha  = db.StringProperty()
    nilai_maks_pinjaman  = db.StringProperty()
    jangka_wkt_pinjaman  = db.StringProperty()
    margin_bunga  = db.StringProperty()
    bantuan_penerima_mamfaat_jfpr  = db.StringProperty()
    manajemen_usaha = db.IntegerProperty(default=0)
    pembukuan = db.IntegerProperty(default=0)
    akses_pasar = db.IntegerProperty(default=0)
    keuangan_mikro = db.IntegerProperty(default=0)
    ao = db.IntegerProperty(default=0)
    cs = db.IntegerProperty(default=0)
    tl = db.IntegerProperty(default=0)
    kelayakan_usaha = db.IntegerProperty(default=0)
    
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())
"""

"""
Group Report include the historical database
"""
"""
class Report_Group(search.SearchableModel, db.Expando):
    livecluster = db.ReferenceProperty(LiveCluster, collection_name='group_report')
    containers = db.ListProperty(db.Key,default=[])
    name_group = db.ReferenceProperty(LiveGroup, collection_name='group_report')
    #added by Jufri Wahyudi
    name = db.StringProperty()
    year = db.StringProperty()
    info = db.TextProperty()
    #end of added

class PersonTraining(search.SearchableModel):
    person = db.ReferenceProperty(Person, collection_name='training')
    manajemen_usaha = db.IntegerProperty(default=0)
    pembukuan = db.IntegerProperty(default=0)
    produksi = db.IntegerProperty(default=0)
    pemanfaatan_limbah = db.IntegerProperty(default=0)
    pengemasan = db.IntegerProperty(default=0)
    akses_pasar = db.IntegerProperty(default=0)
    keuangan_mikro = db.IntegerProperty(default=0)
    hitung_hpp_harga_jual = db.IntegerProperty(default=0)  
    navigasi = db.IntegerProperty(default=0)
    keselamatan_laut = db.IntegerProperty(default=0)
    penanganan_atas_kapal = db.IntegerProperty(default=0)
    kontrol_kualitas = db.IntegerProperty(default=0)
    rawat_mesin = db.IntegerProperty(default=0)
    rescue = db.IntegerProperty(default=0)

class GroupTraining(search.SearchableModel):
    group = db.ReferenceProperty(LiveGroup, collection_name='g_training')
    manajemen_usaha = db.IntegerProperty(default=0)
    pembukuan = db.IntegerProperty(default=0)
    produksi = db.IntegerProperty(default=0)
    pemanfaatan_limbah = db.IntegerProperty(default=0)
    pengemasan = db.IntegerProperty(default=0)
    akses_pasar = db.IntegerProperty(default=0)
    keuangan_mikro = db.IntegerProperty(default=0)
    hitung_hpp_harga_jual = db.IntegerProperty(default=0)  
    navigasi = db.IntegerProperty(default=0)
    keselamatan_laut = db.IntegerProperty(default=0)
    penanganan_atas_kapal = db.IntegerProperty(default=0)
    kontrol_kualitas = db.IntegerProperty(default=0)
    rawat_mesin = db.IntegerProperty(default=0)
    rescue = db.IntegerProperty(default=0)
"""

""" Member Products """
"""
class Product(search.SearchableModel, db.Expando):
    person = db.ReferenceProperty(Person, collection_name='products')
    livecenter = db.ReferenceProperty(LiveCenter, collection_name='products')
    category = db.ReferenceProperty(LiveCategory, collection_name='products')
    cluster = db.ReferenceProperty(LiveCluster, collection_name='products')
    containers = db.ListProperty(db.Key,default=[])
    name  = db.StringProperty()
    geo_pos = db.GeoPtProperty()
    info = db.TextProperty()
    #added by Jufri Wahyudi
    year = db.StringProperty()
    #end of added
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())
""" 
