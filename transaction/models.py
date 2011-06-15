import datetime
from django.db import models
from people.models import People
from translate.lang import money
from counter.tools import BaseModel


class Transaction(BaseModel):
    person = models.ForeignKey(People, verbose_name='nama')
    day = models.DateField('tanggal', default=datetime.date.today())
    description = models.CharField('keterangan', max_length=100)
    nominal = models.FloatField('nominal')

    class Meta:
        ordering = ['day']

    def __unicode__(self):
        return '%s %s %s %s' % (self.person.name, self.day, self.description, money(int(self.nominal)))
