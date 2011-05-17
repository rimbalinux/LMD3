from google.appengine.ext import db
from django.db import models


""" Sharded Counters """
class Counters(db.Model):
    name = db.StringProperty()
    count = db.IntegerProperty(required=True, default=0)
    last_update = db.DateTimeProperty(auto_now=True)


class Counter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s = %d' % (self.name, self.count)



