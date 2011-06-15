from django.db import models
from counter.tools import BaseModel
from livecenter.models import Livelihood, Cluster, Category
from livecenter.tools import GeoModel
from attachment.tools import PhotoModel
from people.models import People


class Type(PhotoModel):
    name = models.CharField('jenis produk', max_length=100, unique=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count','name']

    def __unicode__(self):
        return '%s %d' % (self.name, self.count)


class Product(GeoModel):
    name = models.CharField('nama produk', max_length=100)
    livecenter = models.ForeignKey(Livelihood)
    category = models.ForeignKey(Category, verbose_name='kategori')
    person = models.ForeignKey(People, verbose_name='nama anggota')
    cluster = models.ForeignKey(Cluster, null=True, verbose_name='gugusan')
    info = models.TextField('keterangan')
    year = models.IntegerField('tahun', null=True, blank=True)
    type = models.ForeignKey(Type, verbose_name='tipe')

    def before_save(self, *args, **kwargs):
        super(Product, self).before_save(*args, **kwargs)
        self.livecenter = self.person.livecenter
        self.cluster = self.person.group and self.person.group.cluster or None

    def after_save(self, *args, **kwargs):
        super(Product, self).after_save(*args, **kwargs)
        self.type_counter(1)

    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
        self.type_counter(-1)

    def type_counter(self, value):
        t = Type.objects.filter(id=self.type.id).get()
        t.count += value 
        t.save()

"""
class Container(models.Model):
    new = models.ForeignKey(Product)
    old = models.CharField(max_length=100, unique=True) # livecenter.Product.__key__
"""
