from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from globalrequest.middleware import get_request
from .utils import reset, get, increment, decrement


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True

    @classmethod
    def counter_name(self):
        return 'row_%s' % self._meta.db_table

    @classmethod
    def counter_reset(self):
        reset(self.counter_name())

    @classmethod
    def counter_value(self):
        return get(self.counter_name())

    def before_save(self, is_insert=True):
        self.is_insert = is_insert
        self.updated = datetime.now()
        self.user = get_request().user

    def after_save(self):
        if self.is_insert:
            increment(self.counter_name())

    def save(self, *args, **kwargs):
        self.before_save(not self.pk)
        super(BaseModel, self).save(*args, **kwargs)
        self.after_save()

    def delete(self, *args, **kwargs):
        self.before_delete()
        super(BaseModel, self).delete(*args, **kwargs)
        self.after_delete()

    def before_delete(self):
        pass

    def after_delete(self):
        decrement(self.counter_name())


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = get_request()
        if self.request.POST:
            super(BaseForm, self).__init__(self.request.POST, *args, **kwargs)
        else:
            super(BaseForm, self).__init__(*args, **kwargs)
        if 'photo' in self.fields:
            del self.fields['photo']

