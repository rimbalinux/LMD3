#!/usr/bin/env python
# 
# livelihood producer utils
# author: rudi harsono <sepidol@gmail.com>
# created at: 20100505
#
# changed by: sugiana@gmail.com, 2011-04-25
#

from .models import LivelihoodLocation
from django.http import HttpResponseRedirect
import urllib


def getLocation(id):
    try:
        return LivelihoodLocation().all().filter('dl_id = ',int(id)).get()
    except:
        return

def getLocationKey(id):
    location = getLocation(id)
    return location and location.key() or None

def redirect(request, default_url='/'):
    return HttpResponseRedirect('destination' in request.GET and \
            urllib.unquote(request.GET['destination']) or default_url)
