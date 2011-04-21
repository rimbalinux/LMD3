from google.appengine.ext import search, db
from livecenter.models import Person, LiveCenter, LiveCategory, LiveCluster


""" Member Products """
class Product(search.SearchableModel, db.Expando):
    person = db.ReferenceProperty(Person, collection_name='products')
    livecenter = db.ReferenceProperty(LiveCenter, collection_name='products')
    category = db.ReferenceProperty(LiveCategory, collection_name='products')
    cluster = db.ReferenceProperty(LiveCluster, collection_name='products')
    containers = db.ListProperty(db.Key,default=[])
    name  = db.StringProperty()
    geo_pos = db.GeoPtProperty()
    info = db.TextProperty()
    #added by Jufri Wahyudi
    year = db.StringProperty()
    #end of added
    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())
 
