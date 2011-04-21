from google.appengine.ext import db

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
