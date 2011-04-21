from google.appengine.ext import db


""" Sharded Counters """
class Counters(db.Model):
    name = db.StringProperty()
    count = db.IntegerProperty(required=True, default=0)
    last_update = db.DateTimeProperty(auto_now=True)
