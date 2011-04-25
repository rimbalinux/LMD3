#!/usr/bin/env python
# 
# livelihood producer utils
# author: rudi harsono <sepidol@gmail.com>
# created at: 20100505
#
# changed by: sugiana@gmail.com, 2011-04-25
#

from google.appengine.ext import db
from .models import LivelihoodLocation, Attachment, GeoPosition

def getLocationName(id):
    location = None
    try:
        locationnames = LivelihoodLocation().all().filter('dl_id = ',int(id)).fetch(1000)
        for locationname in locationnames:
            location = locationname.dl_name
    except:
        pass
    return location


def getLocation(id):
    location = None
    try:
        location = LivelihoodLocation().all().filter('dl_id = ',int(id)).get()
    except:
        pass
    return location

def save_file_upload(request, field, container, ftype='photo'):
    if request.get(field):
        att = Attachment.all().filter('containers', container.key()).get()
        if not att:
            att = Attachment()
        att.containers.append(container.key())
        att.filename = 'photo_%s' % container.key().id()
        att.filesize = 1024
        att.file = db.Blob(request.get(field))
        att.put()
    return True

def save_geo_pos(request, field, container, ftype='home'):
    if request.get(field):
        entity = GeoPosition.all().filter('containers', container.key()).get()
        if not entity:
            entity = GeoPosition()
        entity.containers.append(container.key())
        entity.geotype = ftype
        entity.geo_pos = request.get(field)
        entity.put()
    return True
    
