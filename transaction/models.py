from django.db import models
from django.contrib.auth.models import User
from livecenter.models import Person
from translate.lang import money
from google.appengine.ext import db 


def persons():
    r = ()
    for p in Person.all().fetch(10):
        r += (str(p.key()), p.name),
    return r


class Transaction(models.Model):
    person = models.CharField(max_length=100, choices=persons()) # references livecenter.models.Person
    date = models.DateField()
    description = models.CharField(max_length=100)
    nominal = models.FloatField()
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        p = db.get(self.person)
        return '%s %s %s %s' % (p.name, self.date, self.description, money(int(self.nominal)))
