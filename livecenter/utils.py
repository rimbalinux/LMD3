#!/usr/bin/env python
# 
# livelihood producer utils
# author: rudi harsono <sepidol@gmail.com>
# created at: 20100505
#
# changed by: sugiana@gmail.com, 2011-04-25
#

from django.http import HttpResponseRedirect
import urllib
from attachment.models import File
from .settings import DEFAULT_LOCATION
#from .models import LivelihoodLocation


def default_location(geo_pos=None):
    return geo_pos and str(geo_pos).strip('nan,nan') or \
           ', '.join(map(lambda x: str(x), DEFAULT_LOCATION))

"""
def getLocation(id):
    try:
        return LivelihoodLocation().all().filter('dl_id = ',int(id)).get()
    except:
        return

def getLocationKey(id):
    location = getLocation(id)
    return location and location.key() or None
"""

def redirect(request, default_url='/'):
    return HttpResponseRedirect(getattr(request, 'GET') and \
            'destination' in request.GET and \
            urllib.unquote(request.GET['destination']) or default_url)

"""
def migrate_photo(request, source):
    photo = source.photo[:1]
    if photo:
        photo = photo[0]
        photo = File(name=photo.filename, content=photo.file,
            mime='image/png', size=len(photo.file), user=request.user)
        photo.save()
        return photo
"""

