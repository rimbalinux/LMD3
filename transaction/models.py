from django.db import models
from people.models import People
from translate.lang import money
from counter.tools import BaseModel


class Transaction(BaseModel):
    person = models.ForeignKey(People)
    date = models.DateField()
    description = models.CharField(max_length=100)
    nominal = models.FloatField()

    def __unicode__(self):
        return '%s %s %s %s' % (self.person.name, self.date, self.description, money(int(self.nominal)))
