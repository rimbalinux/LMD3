from google.appengine.ext import db
from django.db import models
from djangotoolbox import fields
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

    def __unicode__(self):
        return '%s %d bytes' % (self.name, self.size)

