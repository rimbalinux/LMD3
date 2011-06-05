from attachment.tools import PhotoModel, PhotoForm
from django.db import models


class GeoModel(PhotoModel):
    geo_pos = models.CharField('koordinat GPS', max_length=100, blank=True)

    class Meta:
        abstract = True

    def before_save(self, *args, **kwargs):
        super(GeoModel, self).before_save(*args, **kwargs)
        if self.geo_pos == '0.0,0.0':
            self.geo_pos = ''


class GeoForm(PhotoForm):
    def __init__(self, *args, **kwargs):
        super(GeoForm, self).__init__(*args, **kwargs)
        self.fields['geo_pos'].widget.attrs = {'size': 40}
        
