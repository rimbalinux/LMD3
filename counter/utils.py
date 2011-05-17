#!/usr/bin/env python
# 
# Author: <sugiana@gmail.com>
# Created: 2011-05-13 
#

from .models import Counter

def get(name):
    c = Counter.objects.filter(name=name)
    if c:
        return c.get().count
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


