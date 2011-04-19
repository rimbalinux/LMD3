# Sumber: LMD/models.py

from google.appengine.ext import db

class Users(db.Model):
    username = db.StringProperty()
    passwd = db.StringProperty()
    email  = db.StringProperty()
    fullname = db.StringProperty()
    address = db.TextProperty()
    phone  = db.StringProperty()
    role   = db.IntegerProperty(default=99)
    livecenter = db.ListProperty(db.Key,default=[])

