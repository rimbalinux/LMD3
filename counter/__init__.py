#!/usr/bin/env python
# 
# livelihood producer utils
# author: rudi harsono <sepidol@gmail.com>
# created at: 20100505
#

from .models import Counters

def get(name):
    c = Counters.all().filter('name', name).get()
    if not c:
        return 0
    return c.count

def update(name, value):
    c = Counters.all().filter('name', name).get()
    
    if not c:
        c = Counters()
        c.name = name
        c.count = value
    else:
        c.count += value
    c.save()

def reset(name):
    c = Counters.all().filter('name', name).get()
    if not c:
        return
    c.count = 0
    c.save()    
