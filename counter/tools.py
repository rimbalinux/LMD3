from django.db import models
from .utils import reset, get, increment, decrement


class BaseModel(models.Model):
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

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)
        increment(self.counter_name())

    def delete(self, *args, **kwargs):
        super(BaseModel, self).delete(*args, **kwargs)
        decrement(self.counter_name())

