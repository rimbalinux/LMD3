#!/usr/bin/env python
# 
# Author: <sugiana@gmail.com>
# Created: 2011-05-13 
#

from .models import Counter
from django.core.exceptions import ObjectDoesNotExist

def get(name):
    try:
        c = Counter.objects.get(name=name)
        return c.count
    except ObjectDoesNotExist:
        return 0

def update(name, value):
    c = Counter.objects.filter(name=name)
    if c:
        c = c.get()
        c.count += value
    else:
        c = Counter(name=name, count=value)
    c.save()

def reset(name):
    update(name, 0)

def increment(name):
    update(name, 1)

def decrement(name):
    update(name, -1)


