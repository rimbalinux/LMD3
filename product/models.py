from django.db import models
from counter.tools import BaseModel
from livecenter.models import Livelihood, Cluster, Category
from livecenter.tools import GeoModel
from people.models import People


class Type(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count','name']

    def __unicode__(self):
        return '%s %d' % (self.name, self.count)


class Product(GeoModel):
    name = models.CharField(max_length=100)
    livecenter = models.ForeignKey(Livelihood)
    category = models.ForeignKey(Category)
    person = models.ForeignKey(People)
    cluster = models.ForeignKey(Cluster, null=True)
    info = models.TextField()
    year = models.IntegerField(null=True)
    type = models.ForeignKey(Type)

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


class Container(models.Model):
    new = models.ForeignKey(Product)
    old = models.CharField(max_length=100, unique=True) # livecenter.Product.__key__
