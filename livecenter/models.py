# Sumber: LMD/models.py

from google.appengine.ext import db


""" Location data """
class LivelihoodLocation(db.Model):
    dl_id = db.IntegerProperty()
    dl_name = db.StringProperty()
    dl_parent = db.IntegerProperty()

""" 
LC Centers 
1 LC has many categories
"""
class LiveCenter(db.Model):
    category = db.ListProperty(db.Key,default=[])
    name = db.StringProperty()
    address = db.TextProperty()
    district = db.ReferenceProperty(LivelihoodLocation, collection_name="district")
    sub_district = db.ReferenceProperty(LivelihoodLocation, collection_name="sub_district")
    village = db.ReferenceProperty(LivelihoodLocation, collection_name="village")
    description = db.TextProperty()
    geo_pos = db.GeoPtProperty()
    last_modified = db.DateTimeProperty(auto_now=True)

    @property
    def categories(self):
        return LiveCategory.gql("WHERE __key__ IN :1", self.category)

    @property
    def photo(self):
        return Attachment.gql("WHERE containers = :1", self.key())

    @property
    def productFields(self):
        return MetaForm.gql("WHERE livecenter = :1 AND meta_type = :2", self.key(), 'product')

    @property
    def groupFields(self):
        return MetaForm.gql("WHERE livecenter = :1 AND meta_type = :2", self.key(), 'group')
    
    @property
    def clusters(self):
        return LiveCluster.gql("WHERE livecenter = :1", self.key())

    @property
    def groups(self):
        return LiveGroup.gql("WHERE containers = :1", self.key())
