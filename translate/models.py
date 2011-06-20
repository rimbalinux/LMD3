from django.db import models
from textwrap import wrap

MAX_TEASER_LENGTH = 100 

class Dictionary(models.Model):
    input_lang = models.CharField(max_length=2)
    input = models.TextField()
    output_lang = models.CharField(max_length=2)
    output = models.TextField()

    def __unicode__(self):
        t = wrap(self.input, MAX_TEASER_LENGTH)
        s = t and t[0] or ''
        return t[1:] and '%s ...' % s or s 


