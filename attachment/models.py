from google.appengine.ext import db
from django.db import models
from djangotoolbox import fields
from django.contrib.auth.models import User
from counter.tools import BaseModel

"""
Attachment Storage Center 
User uploaded file storage
"""
class Attachment(db.Model):
    containers  = db.ListProperty(db.Key,default=[])
    doctype     = db.StringProperty(default='photo')
    filename    = db.StringProperty()
    filesize    = db.IntegerProperty()  #in byte
    file        = db.BlobProperty()

class File(BaseModel):
    name = models.CharField(max_length=255)
    mime = models.CharField(max_length=255)
    size = models.IntegerField()
    content = fields.BlobField()
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s %s %d bytes' % (self.name, self.mame, self.size)


class Container(models.Model):
    file = models.ForeignKey(File, unique=True)
    container = models.CharField(max_length=100) # references AnyClass.__key__

