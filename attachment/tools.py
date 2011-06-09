from django.db import models
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from counter.tools import BaseModel
from globalrequest.middleware import get_request
from .models import File
from .utils import save_file_upload


class PhotoModel(BaseModel):
    photo = models.ForeignKey(File, null=True, blank=True, verbose_name='foto')

    class Meta:
        abstract = True

    def before_save(self, *args, **kwargs):
        super(PhotoModel, self).before_save(*args, **kwargs)
        if self.is_insert:
            return
        try:
            old = self.__class__.objects.get(pk=self.pk)
            photo = old.photo
        except ObjectDoesNotExist:
            return
        if not old.photo or not self.photo:
            return
        if old.photo.id != self.photo.id:
            old.photo.delete()

    def delete(self, *args, **kwargs):
        super(PhotoModel, self).delete(*args, **kwargs)
        if self.photo:
            f = File.objects.get(pk=self.photo.id)
            f.delete()


class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = get_request()
        if self.request.POST:
            super(PhotoForm, self).__init__(self.request.POST, *args, **kwargs)
        else:
            super(PhotoForm, self).__init__(*args, **kwargs)
        if 'photo' in self.fields:
            del self.fields['photo']

    def save(self, *args, **kwargs):
        super(PhotoForm, self).save(*args, **kwargs)
        if 'photo_file' in self.request.FILES:
            self.instance.photo = save_file_upload(self.request)
            self.instance.save()


